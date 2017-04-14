from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from bojv4.conf import LANGUAGE

from .models import Submission, CaseResult
from .serializers import SubmissionSerializer

from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import BasePermission

from problem.models import Problem
from django.shortcuts import get_object_or_404
from .forms import SubmissionForm
from django_tables2 import RequestConfig
from .tables import SubmissionTable
import json
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

    def get_context_data(self, **kwargs):
        context = super(SubmissionListView, self).get_context_data(**kwargs)
        submissions_table = SubmissionTable(self.get_queryset())
        RequestConfig(self.request).configure(submissions_table)
        #  add filter here
        context['submissions_table'] = submissions_table
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
        if self.object.cases.count() < self.object.problem.cases.count():
            cases.append({
                'status': 'Judging',
                'position': self.object.cases.count(),
                'time': 0,
                'memory': 0,
            })
        context['cases'] = cases
        return context


class SubmissionCreateView(CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name_suffix = '_create_form'

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
        logger.warning("=================form save===============\n")
        self.object = form.save(commit=False)
        self.object.problem = self.problem
        self.object.user = self.request.user
        print self.object.code
        logger.warning("=================start save===============\n")
        self.object.save()
        logger.warning("=================judge===============\n")
        try:
            self.object.judge()
            logger.warning("=================judge end===============\n")
        except Exception as ex:
            logger.warning(ex)
        return super(SubmissionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('submission:submission-list')


