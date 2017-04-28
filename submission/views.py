from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from bojv4.conf import LANGUAGE

from .models import Submission, CaseResult
from .forms import SubmissionForm
from .serializers import SubmissionSerializer
from .tables import SubmissionTable
from .filters import SubmissionFilter

from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user
from django_tables2 import RequestConfig

from problem.models import Problem
from ojuser.models import GroupProfile
import logging
logger = logging.getLogger('django')
#  from guardian.shortcuts import get_objects_for_user


class SubmissionPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return obj.problem.view_by_user(user=request.user)


class CaseResultPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return obj.submission.problem.view_by_user(user=request.user)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated,)


class SubmissionListView(ListView):

    model = Submission
    paginate_by = 20

    def get_queryset(self):
        groups = get_objects_for_user(self.user, 'ojuser.change_groupprofile', GroupProfile)
        ans = self.user.submissions.all()
        for g in groups:
            for p in g.problems.all():
                ans |= p.submissions.all()
        res = reduce(lambda x, y : x | y, map(lambda x: x.problems.all(), groups)).distinct()
        self.submission_can_view_qs = ans.distinct()
        print self.request.GET
        self.filter = SubmissionFilter(
            self.request.GET,
            queryset=self.submission_can_view_qs,
            problems=res
        )
        print "filters=========="
        print self.filter.filters
        # self.filter.filters.get('problem').queryset = res
        return self.filter.qs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(SubmissionListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SubmissionListView, self).get_context_data(**kwargs)
        submissions_table = SubmissionTable(self.get_queryset())
        RequestConfig(self.request).configure(submissions_table)
        #  add filter here
        context['submissions_table'] = submissions_table
        0
        #  add filter here
        context['filter'] = self.filter
        context['submission_can_view'] = self.submission_can_view_qs

        return context


class SubmissionDetailView(DetailView):

    model = Submission
    permission_classes = (IsAuthenticated, SubmissionPermission)

    @method_decorator(login_required)
    def dispatch(self, request, pid=None, *args, **kwargs):
        self.user = request.user
        return super(SubmissionDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        logger.warning('============test===============')
        status = self.object.get_status_display()
        if self.object.status == 'JD':
            status = 'Judging in ' + str(self.object.cases.count()) + 'th case'
        context = super(SubmissionDetailView, self).get_context_data(**kwargs)
        context['status'] = status
        cases = []
        for c in self.object.cases.all():
            cases.append({
                'status': c.status,
                'position': c.position,
                'time': c.running_time,
                'memory': c.running_memory,
            })
        if self.object.status == 'JD' and self.object.cases.count() < self.object.problem.cases.count():
            cases.append({
                'status': 'Judging',
                'position': self.object.cases.count(),
                'time': 0,
                'memory': 0,
            })
        context['cases'] = cases
        return context


class SubmissionCreateView(SuccessMessageMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name_suffix = '_create_form'
    success_message = "your submission has been created successfully"

    @method_decorator(login_required)
    def dispatch(self, request, pid=None, *args, **kwargs):
        pid = self.kwargs['pid']
        self.problem = Problem.objects.filter(pk=pid).first()
        if not self.problem:
            print "no problem"
        else:
            print "have p, ", request.user.username
        if not self.problem or not self.problem.view_by_user(request.user):
            raise Http404("Problem does not exist")
        if not self.problem.is_checked:
            return HttpResponseForbidden()
        self.user = request.user
        return super(SubmissionCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kw = super(SubmissionCreateView, self).get_form_kwargs()
        kw['qs'] = LANGUAGE.choice()
        return kw

    def get_context_data(self, **kwargs):
        context = super(SubmissionCreateView, self).get_context_data(**kwargs)
        context['problem'] = self.problem
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.problem = self.problem
        self.object.user = self.request.user
        print self.object.code
        try:
            self.object.save()
            self.object.judge()
        except Exception as ex:
            logger.warning(ex)
        return super(SubmissionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('submission:submission-list')


