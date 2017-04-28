from datetime import datetime, timedelta
import json
import math
from .models import Contest, ContestProblem, ContestSubmission
from .filters import ContestFilter
from .tables import ContestTable
from .forms import ContestForm, SubmissionForm

from problem.models import Problem
from submission.models import Submission
from bojv4.conf import LANGUAGE_MASK, LANGUAGE

from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from guardian.shortcuts import get_objects_for_user
from django_tables2 import RequestConfig

from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.request import Request
# Create your views here.


class ContestViewPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Contest):
            print "Not Problem"
            return False
        if request.user.has_perm('ojuser.change_groupprofile', obj.group):
            return True
        print type(obj.start_time)
        now = datetime.now()
        if request.user.has_perm('ojuser.view_groupprofile', obj.group) and now > obj.start_time.replace(tzinfo=None)\
                and now < obj.start_time.replace(tzinfo=None) + timedelta(minutes=obj.length):
            return True
        return False

class ContestChangePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        pass


class SubmissionPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, ContestSubmission):
            print "Not Problem"
            return False
        if request.user == obj.user:
            return True
        group = obj.problem.contest.group
        return request.user.has_perm('ojuser.change_groupprofile', group)


class ContestViewSet(ModelViewSet):
    queryset = Contest.objects.all()
    permission_classes = (IsAuthenticated, ContestViewPermission)

    def get_queryset(self):
        return self.queryset

    @detail_route(methods=['get'], url_path='board')
    def get_contest_board(self, request, pk=None):
        contest = self.get_object()
        subs = ContestSubmission.objects.filter(problem__contest=contest).all()
        probs = ContestProblem.objects.filter(contest=contest).all()
        info = {}
        for csub in subs:
            sub = csub.submission
            uid = sub.user.username
            idx = csub.problem.index
            if sub.status in ['PD', 'JD', 'CL', 'SE']:
                continue

            uinfo = info.get(uid, None)
            if not uinfo:
                uinfo = {'username': uid, 'nickname': sub.user.profile.nickname}
                info[uid] = uinfo
            pinfo = uinfo.get('pinfo', None)
            if not pinfo:
                pinfo = {}
                uinfo['pinfo'] = pinfo
            sinfo = pinfo.get(idx, None)
            if not sinfo:
                sinfo = {'idx': idx, 'AC': 0, 'sub': 0, 'pen': 0}
                pinfo[idx] = sinfo
            if sinfo.get('AC', 0):
                continue
            td = sub.create_time - contest.start_time
            info[uid]['pinfo'][idx]['sub'] += 1
            if sub.status == "AC":
                info[uid]['pinfo'][idx]["AC"] = info[uid]['pinfo'][idx]['sub']
                info[uid]['pinfo'][idx]["ac_time"] = int(math.ceil(td.total_seconds() / 60))
                # info[uid]['pinfo'][idx]["pen"] += int(math.ceil(td.total_seconds() / 60))
            else:
                info[uid]['pinfo'][idx]["AC"] -= 1
                info[uid]['pinfo'][idx]["pen"] += 20

        info = info.values()

        for i in info:
            for prob in probs:
                if not i['pinfo'].has_key(prob.index):
                    i['pinfo'] = {
                        'idx': prob.idx,
                        'AC': 0,
                        'sub': 0,
                        'pen': 0
                    }
            i['pinfo'] = i['pinfo'].values()
            i['pinfo'].sort(key=lambda x: x['idx'])
            i['sub'] = 0
            i['AC'] = 0
            i['pen'] = 0
            for sinfo in i['pinfo']:
                print sinfo
                if sinfo.get('AC', 0) > 0:
                    i['AC'] += 1
                    i['pen'] += sinfo.get('pen', 0) + sinfo.get('ac_time', 0)
                i['sub'] += sinfo.get('sub', 0)

        return Response(info)

    @detail_route(methods=['post'], url_path='submit')
    def create_submission(self, request, pk=None):
        print self.get_object().title
        print request.POST
        index = request.POST.get('index', '')
        code = request.POST.get('code', '')
        s = Submission()
        s.length = len(code)
        if s.length > Submission.CODE_LENGTH_LIMIT:
            messages.add_message(
                request._request,
                messages.ERROR,
                _('Code length exceed limit')
            )
            print request.META['HTTP_REFERER']
            return HttpResponseRedirect(reverse('contest:submission-add', args=(pk,)))

        language = request.POST.get('language')
        p = ContestProblem.objects.filter(contest=self.get_object(), index=index).first()
        s.code = code
        s.problem = p.problem
        s.language = language
        s.user = request.user
        s.save()
        cs = ContestSubmission()
        cs.submission = s
        cs.problem = p
        cs.save()
        s.judge()
        messages.add_message(
            request._request,
            messages.SUCCESS,
            _('Submit Success')
        )
        return HttpResponseRedirect(reverse('contest:submission-list', args=(pk, )))


class ContestListView(ListView):

    model = Contest
    paginate_by = 10

    def get_queryset(self):
        group_can_view_qs = get_objects_for_user(
            self.request.user,
            'ojuser.view_groupprofile',
            with_superuser=True
        ).distinct()
        self.contest_can_view_qs = self.request.user.contests.all()
        for g in group_can_view_qs.all():
            self.contest_can_view_qs |= g.contests.all()
        self.filter = ContestFilter(
            self.request.GET,
            queryset=self.contest_can_view_qs,
            user=self.request.user
        )
        return self.filter.qs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        print self.template_name
        return super(ContestListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContestListView, self).get_context_data(**kwargs)
        contests_table = ContestTable(self.get_queryset())
        RequestConfig(self.request).configure(contests_table)
        #  add filter here
        context['contests_table'] = contests_table
        context['filter'] = self.filter
        context['contests_can_view'] = self.contest_can_view_qs
        print "_________________filter"
        # context['contests_can_delete'] = self.contest_can_delete_qs
        # context['contests_can_change'] = self.contest_can_change_qs
        return context


class ContestCreateView(SuccessMessageMixin, TemplateView):
    template_name = 'contest/contest_create_form.html'
    success_message = "your Contest has been created successfully"
    permission_classes = (IsAuthenticated, )

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        print "=====================args============"
        gid = kwargs.get('gid')
        try:
            gid = int(gid)
        except Exception as ex:
            print ex
            gid = -1
        self.group = get_object_or_404(get_objects_for_user(request.user, 'ojuser.change_groupprofile', with_superuser=True), pk=gid)
        return super(ContestCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        print "=================HTTP method: ", request.method
        if request.method == 'POST':
            form = ContestForm(request.POST)
            print request.POST
            if form.is_valid():
                problem_list = request.POST.getlist('problem_id')
                score_list = request.POST.getlist('problem_score_custom')
                score_list = map(lambda x: int(x), score_list)
                problem_list = map(lambda x: int(x), problem_list)
                c = Contest()
                c.author = request.user
                c.start_time = datetime.combine(form.cleaned_data['start_date'], form.cleaned_data['start_time'])
                c.board_stop = form.cleaned_data['board_stop']
                c.desc = form.cleaned_data['desc']
                c.length = form.cleaned_data['length']
                c.group = self.group
                c.title = form.cleaned_data['title']
                for x in form.cleaned_data['lang_limit']:
                    c.lang_limit |= int(x)
                c.save()
                problem_tile_list = request.POST.getlist('problem_title_custom')
                pindex = 'ABCDEFGHIJKLMNOPQRSTUVWSYZ'
                for i in range(len(problem_list)):
                    p = Problem.objects.filter(pk=problem_list[i]).first()
                    if ContestProblem.objects.filter(problem=p, contest=c).count() > 0 or not p:
                        print "Error Problem, ", problem_list[i]
                        continue
                    cp = ContestProblem()
                    cp.problem = p
                    cp.title = problem_tile_list[i]
                    cp.score = score_list[i]
                    cp.contest = c
                    cp.index = pindex[i]
                    cp.save()
                print "____________________end__________________"
                print reverse('contest:contest-list')
                return HttpResponseRedirect(reverse('contest:contest-list'))
        return super(ContestCreateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ContestCreateView, self).get_context_data(**kwargs)
        context['now'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        context['form'] = ContestForm()
        groups = get_objects_for_user(self.request.user, 'ojuser.change_groupprofile', with_superuser=True)
        control_problem = None
        for g in groups:
            if not control_problem:
                control_problem = g.problems.all()
            else:
                control_problem |= g.problems.all()
        context['control_problem'] = control_problem.distinct() if control_problem else None
        print context['now']
        return context


class ContestDetailView(DetailView):
    model = Contest
    permission_classes = (IsAuthenticated, ContestViewPermission)

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        # self.object = get_object_or_404(self.get_queryset(), pk=pk)
        return super(ContestDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContestDetailView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['is_admin'] = self.request.user.has_perm('ojuser.change_groupprofile', self.object.group)
        return context


class ProblemDetailView(DetailView):
    model = Contest
    permission_classes = (IsAuthenticated, ContestViewPermission)
    template_name = 'contest/problem_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', -1)
        index = kwargs.get('index', '#')
        print index
        self.problem = ContestProblem.objects.filter(contest__pk=pk, index=index).first()
        if not self.problem:
            raise Http404
        return super(ProblemDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(**kwargs)
        context['problem'] = self.problem
        return context


class SubmissionListView(DetailView):
    model = Contest
    permission_classes = (IsAuthenticated, ContestViewPermission)
    template_name = 'contest/submission_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SubmissionListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionListView, self).get_context_data(**kwargs)
        # context['submissions'] = reduce(lambda x, y: (x.submissions.all() | y.submissions.all()), self.object.problems.all())
        if self.request.user.has_perm('ojuser.change_groupprofile', self.object.group):
            context['submissions'] = ContestSubmission.objects.filter(problem__contest=self.object).all()
        else:
            context['submissions'] = ContestSubmission.objects.filter(problem__contest=self.object, submission__user=self.request.user).all()
        return context


class ClarificationListView(DetailView):
    model = Contest
    permission_classes = (IsAuthenticated, ContestViewPermission)


class BoardView(DetailView):
    model = Contest
    permission_classes = (IsAuthenticated, ContestViewPermission)
    template_name = 'contest/board2.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BoardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)
        # context['submissions'] = reduce(lambda x, y: (x.submissions.all() | y.submissions.all()), self.object.problems.all())
        context['problems'] = self.object.problems.all()
        return context


class ContestUpdateView(TemplateView):
    template_name = 'contest/contest_create_form.html'
    success_message = "your Contest has been updated successfully"
    permission_classes = (IsAuthenticated, )

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        groups = get_objects_for_user(self.request.user, 'ojuser.change_groupprofile', with_superuser=True)
        qs = Contest.objects.filter(group__in=groups)
        self.object = get_object_or_404(qs, pk=pk)
        return super(ContestUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print "=================HTTP method: ", request.method
        if request.method == 'POST':
            form = ContestForm(request.POST)
            if form.is_valid():
                problem_list = request.POST.getlist('problem_id')
                score_list = request.POST.getlist('problem_score_custom')
                score_list = map(lambda x: int(x), score_list)
                problem_list = map(lambda x: int(x), problem_list)
                self.object.author = request.user
                self.object.start_time = datetime.combine(form.cleaned_data['start_date'], form.cleaned_data['start_time'])
                self.object.board_stop = form.cleaned_data['board_stop']
                self.object.desc = form.cleaned_data['desc']
                self.object.length = form.cleaned_data['length']
                self.object.group = self.group
                self.object.title = form.cleaned_data['title']
                for x in form.cleaned_data['lang_limit']:
                    self.object.lang_limit |= int(x)
                self.object.save()
                problem_tile_list = request.POST.getlist('problem_title_custom')
                pindex = 'ABCDEFGHIJKLMNOPQRSTUVWSYZ'
                problem_pks = []
                for i in range(len(problem_list)):
                    p = Problem.objects.filter(pk=problem_list[i]).first()
                    cp = ContestProblem.objects.filter(contest=self.object, index=pindex).first()
                    if not cp:
                        cp = ContestProblem()
                    cp.problem = p
                    cp.title = problem_tile_list[i]
                    cp.score = score_list[i]
                    cp.contest = self.object
                    cp.index = pindex[i]
                    cp.save()
                    problem_pks.append(cp.pk)

                for p in self.object.problems.all():
                    if p.pk not in problem_pks:
                        p.delete()
                print reverse('contest:contest-list')
                return HttpResponseRedirect(reverse('contest:contest-list'))
        context = self.get_context_data(**kwargs)
        return super(ContestUpdateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ContestUpdateView, self).get_context_data(**kwargs)
        context['now'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        context['form'] = ContestForm()
        groups = get_objects_for_user(self.request.user, 'ojuser.change_groupprofile', with_superuser=True)
        control_problem = None
        for g in groups:
            if not control_problem:
                control_problem = g.problems.all()
            else:
                control_problem |= g.problems.all()
        context['control_problem'] = control_problem.distinct() if control_problem else None
        context['problems'] = self.object.problems.all()
        return context


class SubmissionCreateView(DetailView):
    model = Contest
    template_name = 'contest/submission_create_form.html'
    success_message = "your submission has been created successfully"
    permission_classes = (IsAuthenticated, ContestViewPermission)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        print request.GET
        self.index = request.GET.get('index', None)
        return super(SubmissionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionCreateView, self).get_context_data(**kwargs)
        context['index'] = self.index
        form = SubmissionForm()
        form.fields['index'].choices = ((x.index, x.index + '. ' + x.title) for x in self.object.problems.all())
        if self.index:
            form.fields['index'].initial = self.index
        else:
            form.fields['index'].initial = 'A'
        lang_limit = []
        for x in LANGUAGE_MASK.choice():
            if self.object.lang_limit & x[0]:
                lang_limit.append((x[1], LANGUAGE.get_display_name(x[1])))
        form.fields['language'].choices = lang_limit
        context['form'] = form
        return context


class SubmissionDetailView(DetailView):
    model = ContestSubmission
    permission_classes = (IsAuthenticated, SubmissionPermission)
    template_name = 'contest/submission_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, cpk=None, pk=None, *args, **kwargs):
        self.user = request.user
        self.contest = Contest.objects.filter(pk=cpk).first()
        return super(SubmissionDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        submission = self.object.submission
        status = submission.get_status_display()
        if submission.status == 'JD':
            status = 'Judging in ' + str(self.object.cases.count()) + 'th case'
        context = super(SubmissionDetailView, self).get_context_data(**kwargs)
        context['status'] = status
        context['contest'] = self.contest
        cases = []
        for c in submission.cases.all():
            cases.append({
                'status': c.status,
                'position': c.position,
                'time': c.running_time,
                'memory': c.running_memory,
            })
        if submission.status == 'JD' and submission.cases.count() < submission.problem.cases.count():
            cases.append({
                'status': 'Judging',
                'position': submission.cases.count(),
                'time': 0,
                'memory': 0,
            })
        context['cases'] = cases
        return context
