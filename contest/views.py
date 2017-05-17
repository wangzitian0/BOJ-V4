from datetime import datetime, timedelta
import json
import math
from .models import Contest, ContestProblem, ContestSubmission, Notification, Clarification
from .filters import ContestFilter, SubmissionFilter
from .tables import ContestTable, NotificationTable, ClarificationTable, SubmissionTable
from .forms import ContestForm, SubmissionForm, NotificationForm, QuestionForm, AnswerForm
from .serializers import ContestSubmissionSerializer

from problem.models import Problem
from submission.models import Submission
from bojv4.conf import LANGUAGE_MASK, CONTEST_TYPE, CONTEST_CACHE_EXPIRE_TIME, CONTEST_CACHE_FLUSH_TIME
from common.nsq_client import send_to_nsq

from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView
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

    def has_permission(self, request, view):
        print "xxxxxxxxxxxx"

    def has_object_permission(self, request, view, obj):
        print "permission"
        if not isinstance(obj, Contest):
            return False
        if request.user.has_perm('ojuser.change_groupprofile', obj.group):
            return True
        now = datetime.now()
        if request.user.has_perm('ojuser.view_groupprofile', obj.group) and obj.ended() == 0:
            return True
        return False


class ContestChangePermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Contest):
            return False
        if request.user.has_perm('ojuser.change_groupprofile', obj.group):
            return True
        return False


class SubmissionPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, ContestSubmission):
            return False
        if request.user == obj.user:
            return True
        group = obj.problem.contest.group
        return request.user.has_perm('ojuser.change_groupprofile', group)


class ContestViewSet(ModelViewSet):
    queryset = Contest.objects.all()
    permission_classes = (IsAuthenticated, ContestViewPermission)
    serializer_class = ContestSubmissionSerializer

    @detail_route(methods=['post'], url_path='submit')
    def submit(self, request, pk=None):
        print request.data
        send_to_nsq('submit', json.dumps(request.data))
        messages.add_message(
            self.request._request,
            messages.SUCCESS,
            _('Submit Success')
        )
        return Response({'code': 0})

    @detail_route(methods=['get'], url_path='board')
    def get_contest_board(self, request, pk=None):
        contest = self.get_object()

        lock = str(contest.pk) + "__lock"
        if cache.get(lock):
            res = cache.get(contest.key())
            return Response(res)
        cache.set(lock, 1, CONTEST_CACHE_FLUSH_TIME)

        subs = ContestSubmission.objects.filter(problem__contest=contest).all()
        probs = ContestProblem.objects.filter(contest=contest).all()

        mp = {}
        for p in probs:
            mp[p.index] = float(p.score) / max(1, p.problem.score)
        info = {}
        for csub in subs:
            sub = csub.submission
            uid = sub.user.username
            idx = csub.problem.index
            if sub.status in ['PD'  , 'JD', 'CL', 'SE'] or sub.user.has_perm('ojuser.change_groupprofile', contest.group):
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
                if contest.contest_type == CONTEST_TYPE.ICPC:
                    info[uid]['pinfo'][idx]["pen"] += 20
            if contest.contest_type == CONTEST_TYPE.OI:
                info[uid]['pinfo'][idx]["pen"] = max(info[uid]['pinfo'][idx]["pen"], mp[idx] * sub.score)
        info = info.values()

        for i in info:
            for prob in probs:
                if not i['pinfo'].has_key(prob.index):
                    i['pinfo'][prob.index] = {
                        'idx': prob.index,
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
                if sinfo.get('AC', 0) > 0:
                    i['AC'] += 1
                    if contest.contest_type == CONTEST_TYPE.ICPC:
                        i['pen'] += sinfo.get('pen', 0) + sinfo.get('ac_time', 0)
                if contest.contest_type == CONTEST_TYPE.OI:
                    i['pen'] += sinfo.get('pen')
                i['sub'] += sinfo.get('sub', 0)
        if contest.contest_type == CONTEST_TYPE.ICPC:
            info.sort(key=lambda x: x['AC']*1000000-x['pen'], reverse=True)
        else:
            info.sort(key=lambda x: x['pen'], reverse=True)
        cache.set(contest.key(), info, CONTEST_CACHE_EXPIRE_TIME)
        return Response(info)


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
        return super(ContestListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContestListView, self).get_context_data(**kwargs)
        contests_table = ContestTable(self.get_queryset())
        RequestConfig(self.request).configure(contests_table)
        #  add filter here
        context['contests_table'] = contests_table
        context['filter'] = self.filter
        context['contests_can_view'] = self.contest_can_view_qs
        # context['contests_can_delete'] = self.contest_can_delete_qs
        # context['contests_can_change'] = self.contest_can_change_qs
        return context


class ContestCreateView(CreateView):
    template_name = 'contest/contest_create_form.html'
    success_message = "your Contest has been created successfully"
    model = Contest
    form_class = ContestForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        gid = kwargs.get('gid')
        try:
            gid = int(gid)
        except Exception as ex:
            gid = -1
        self.group = get_object_or_404(get_objects_for_user(request.user, 'ojuser.change_groupprofile', with_superuser=True), pk=gid)
        return super(ContestCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        problem_list = self.request.POST.getlist('problem_id')
        score_list = self.request.POST.getlist('problem_score_custom')
        problem_tile_list = self.request.POST.getlist('problem_title_custom')
        score_list = map(lambda x: int(x), score_list)
        problem_list = map(lambda x: int(x), problem_list)
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.lang_limited = form.cleaned_data['lang_limited']
        self.object.group = self.group
        self.object.save()
        pindex = 'ABCDEFGHIJKLMNOPQRSTUVWSYZ'
        for i in range(len(problem_list)):
            p = Problem.objects.filter(pk=problem_list[i]).first()
            if not p or ContestProblem.objects.filter(problem=p, contest=self.object).count() > 0:
                continue
            cp = ContestProblem(problem=p, title=problem_tile_list[i],
                                score=score_list[i], contest=self.object, index=pindex[i])
            cp.save()
        return super(ContestCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContestCreateView, self).get_context_data(**kwargs)
        groups = get_objects_for_user(self.request.user, 'ojuser.change_groupprofile', with_superuser=True)
        control_problem = None
        for g in groups:
            if not control_problem:
                control_problem = g.problems.all()
            else:
                control_problem |= g.problems.all()
        context['control_problem'] = control_problem.distinct() if control_problem else None
        return context

    def get_success_url(self):
        return reverse("contest:contest-detail", args=[self.object.pk])


class ContestDetailView(DetailView):
    model = Contest

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
    template_name = 'contest/problem_detail.html'

    def get_queryset(self):
        return Contest.objects.all()

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        index = kwargs.get('index', '#')
        self.problem = ContestProblem.objects.filter(contest__pk=pk, index=index).first()
        if not self.problem:
            raise Http404
        return super(ProblemDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(**kwargs)
        context['problem'] = self.problem
        if self.request.user.has_perm('ojuser.change_groupprofile', self.object.group):
            context['is_admin'] = True
        return context


class SubmissionListView(ListView):
    model = ContestSubmission
    template_name = 'contest/submission_list.html'
    paginate_by = 15

    def get_queryset(self):
        queryset = None
        if self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            queryset = ContestSubmission.objects.filter(problem__contest=self.contest).all()
        else:
            queryset = ContestSubmission.objects.filter(problem__contest=self.contest, submission__user=self.request.user).all()
        self.filter = SubmissionFilter(
            self.request.GET,
            queryset=queryset,
            problems=self.contest.problems.all()
        )
        return self.filter.qs


    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.contest = get_object_or_404(Contest.objects.filter(group__in=get_objects_for_user(
            request.user,
            'ojuser.view_groupprofile',
            with_superuser=True)), pk=pk)
        return super(SubmissionListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionListView, self).get_context_data(**kwargs)
        submissions_table = SubmissionTable(self.get_queryset())
        # submissions_table.paginate(page=self.request.get('page', 1), per_page=20)
        RequestConfig(self.request).configure(submissions_table)
        #  add filter here
        context['submissions_table'] = submissions_table
        # context['submissions'] = self.filter.qs.order_by('-pk')
        #  add filter here
        context['filter'] = self.filter
        context['contest'] = self.contest
        if self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            context['is_admin'] = True
        return context


class BoardView(DetailView):
    model = Contest
    template_name = 'contest/contest_board.html'

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.contest = Contest.objects.filter(pk=pk).first()
        return super(BoardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BoardView, self).get_context_data(**kwargs)
        # context['submissions'] = reduce(lambda x, y: (x.submissions.all() | y.submissions.all()), self.object.problems.all())
        context['problems'] = self.object.problems.all()
        if self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            context['is_admin'] = True
        return context


class ContestUpdateView(UpdateView):
    template_name = 'contest/contest_create_form.html'
    success_message = "your Contest has been updated successfully"
    form_class = ContestForm
    model = Contest

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.pk = pk
        return super(ContestUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("contest:contest-detail", args=[self.pk])

    def form_valid(self, form):
        problem_list = self.request.POST.getlist('problem_id')
        score_list = self.request.POST.getlist('problem_score_custom')
        problem_tile_list = self.request.POST.getlist('problem_title_custom')
        score_list = map(lambda x: int(x), score_list)
        problem_list = map(lambda x: int(x), problem_list)
        self.object = form.save(commit=False)
        self.object.lang_limited = form.cleaned_data['lang_limited']
        self.object.save()
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
        self.object.save()
        return super(ContestUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContestUpdateView, self).get_context_data(**kwargs)
        context['now'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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

    def get_form_kwargs(self):
        kwargs = super(ContestUpdateView, self).get_form_kwargs()
        d, t = self.object.get_date_time()
        kwargs['initial'] = {
            'lang_limited': self.object.lang_limited,
            'start_date': d,
            'start_time': t,
        }
        return kwargs


class SubmissionCreateView(DetailView):
    template_name = 'contest/submission_create_form.html'
    success_message = "your submission has been created successfully"
    model = Contest

    def get_queryset(self):
        return Contest.objects.all()

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.index = request.GET.get('index', None)
        self.contest = self.get_object()

        return super(SubmissionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionCreateView, self).get_context_data(**kwargs)
        context['contest'] = self.contest
        queryset = None
        if self.index:
            queryset = ContestProblem.objects.filter(contest=self.contest, index=self.index).first()
        else:
            queryset = self.contest.problems.first()
        form = SubmissionForm(initial={'problem': queryset})
        form.set_choice(self.contest)
        context['form'] = form
        if self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            context['is_admin'] = True
        return context


class SubmissionDetailView(DetailView):
    model = ContestSubmission
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


class NotificationListView(DetailView):

    model = Contest
    template_name = 'contest/notification_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        return super(NotificationListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        self.notification_can_view_qs = self.object.notifications.all()
        notifications_table = NotificationTable(self.notification_can_view_qs)
        RequestConfig(self.request).configure(notifications_table)
        context['notification_table'] = notifications_table
        if self.request.user.has_perm('ojuser.change_groupprofile', self.object.group):
            context['is_admin'] = True
        return context


class NotificationCreateView(TemplateView):

    template_name = 'contest/notification_create_form.html'
    success_message = "your notification has been created successfully"

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.contest = Contest.objects.filter(pk=pk).first()
        if not self.contest or not request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            raise Http404()
        return super(NotificationCreateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'POST':
            form = NotificationForm(request.POST)
            if form.is_valid():
                object = form.save(commit=False)
                object.contest = self.contest
                object.author = request.user
                object.save()
                return HttpResponseRedirect(reverse('contest:contest-detail', args=[self.contest.pk, ]))
        return super(NotificationCreateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(NotificationCreateView, self).get_context_data(**kwargs)
        context['form'] = NotificationForm()
        context['contest'] = self.contest
        return context


class NotificationUpdateView(TemplateView):

    template_name = 'contest/notification_create_form.html'
    success_message = "your notification has been created successfully"

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, nid=None, *args, **kwargs):
        self.contest = Contest.objects.filter(pk=pk).first()
        self.notification = Notification.objects.filter(pk=nid).first()
        if not self.contest or not self.notification or not request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            raise Http404()
        return super(NotificationUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.method == 'POST':
            form = NotificationForm(request.POST, instance=self.notification)
            if form.is_valid():
                object = form.save()
                object.contest = self.contest
                object.author = request.user
                object.save()
                return HttpResponseRedirect(reverse('contest:notification-list', args=[self.contest.pk, ]))
        return super(NotificationUpdateView, self).render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(NotificationUpdateView, self).get_context_data(**kwargs)
        context['form'] = NotificationForm(instance=self.notification)
        context['contest'] = self.contest
        return context


class ClarificationListView(ListView):

    model = Contest
    template_name = 'contest/clarification_list.html'

    paginate_by = 15

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.contest = get_object_or_404(Contest.objects.filter(group__in=get_objects_for_user(
            request.user,
            'ojuser.view_groupprofile',
            with_superuser=True)), pk=pk)
        return super(ClarificationListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClarificationListView, self).get_context_data(**kwargs)
        self.clarification_can_view_qs = self.contest.clarifications.all()
        notifications_table = ClarificationTable(self.clarification_can_view_qs)
        RequestConfig(self.request, paginate={'per_page': 20}).configure(notifications_table)
        context['clarification_table'] = notifications_table
        context['contest'] = self.contest
        if self.request.user.has_perm('ojuser.change_groupprofile', self.contest.group):
            context['is_admin'] = True
        return context


class QuestionView(CreateView):

    model = Clarification
    template_name = 'contest/add_clarification.html'
    form_class = QuestionForm
    success_message = "your question has been created successfully"

    @method_decorator(login_required)
    def dispatch(self, request, pk=None, *args, **kwargs):
        self.contest = get_object_or_404(Contest.objects.filter(group__in=get_objects_for_user(
            request.user,
            'ojuser.view_groupprofile',
            with_superuser=True)), pk=pk)
        return super(QuestionView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.contest = self.contest
        self.object.author = self.request.user
        self.object.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            self.success_message
            )
        return super(QuestionView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QuestionView, self).get_context_data()
        context['contest'] = self.contest
        context['form'] = QuestionForm()
        return context

    def get_success_url(self):
        return reverse('contest:contest-detail', args=[self.contest.pk])


class AnswerView(UpdateView):

    model = Clarification
    template_name = 'contest/add_clarification.html'
    form_class = AnswerForm

    @method_decorator(login_required)
    def dispatch(self, request, cpk=None, *args, **kwargs):
        self.contest = get_object_or_404(Contest.objects.filter(group__in=get_objects_for_user(
            request.user,
            'ojuser.change_groupprofile',
            with_superuser=True)), pk=cpk)
        return super(AnswerView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AnswerView, self).get_context_data()
        context['contest'] = self.contest
        context['form'] = self.form_class()
        return context

    def get_success_url(self):
        return reverse('contest:clarification-list', args=[self.contest.pk])


class QuestionDeleteView(DeleteView):
    model = Clarification
    template_name = 'ojuser/group_confirm_delete.html'

    @method_decorator(login_required)
    def dispatch(self, request, cpk=None, *args, **kwargs):
        self.contest = get_object_or_404(Contest.objects.filter(group__in=get_objects_for_user(
            request.user,
            'ojuser.change_groupprofile',
            with_superuser=True)), pk=cpk)
        return super(QuestionDeleteView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('contest:clarification-list', args=[self.contest.pk])

