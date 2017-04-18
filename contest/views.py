from datetime import datetime
import json
from .models import Contest, ContestProblem
from .filters import ContestFilter
from .tables import ContestTable
from .form import ContestForm

from problem.models import Problem

from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig

from guardian.shortcuts import get_objects_for_user
from django.shortcuts import get_object_or_404
# Create your views here.


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
        print "template_name: ", self.get_template_names()
        contests_table = ContestTable(self.get_queryset())
        RequestConfig(self.request).configure(contests_table)
        print "_________________end"
        #  add filter here
        context['contests_table'] = contests_table
        context['filter'] = self.filter
        context['contests_can_view'] = self.contest_can_view_qs
        print "_________________filter"
        # context['contests_can_delete'] = self.contest_can_delete_qs
        # context['contests_can_change'] = self.contest_can_change_qs
        return context

'''
class ContestCreateView(TemplateView):

    template_name_suffix = '_create_form'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ContestCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        group =

'''


class ContestCreateView(SuccessMessageMixin, TemplateView):
    template_name = 'contest/contest_create_form.html'
    success_message = "your Contest has been created successfully"

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
            print "=======================form data"
            print form.is_valid()
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
