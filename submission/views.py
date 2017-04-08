from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from bojv4.conf import LANGUAGE

from .models import Submission
from .serializers import SubmissionSerializer

from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import JsonResponse, HttpResponseNotAllowed, Http404, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from problem.models import Problem
from django.shortcuts import get_object_or_404
from .forms import SubmissionForm
from django_tables2 import RequestConfig
from .tables import SubmissionTable
from common.nsq_client import send_to_nsq 
import logging
import json
logger = logging.getLogger('django')
#  from guardian.shortcuts import get_objects_for_user


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

    def get_context_data(self, **kwargs):
        print __name__
        logger.warning('============test===============')
        logger.info('==================test=========info=======')
        context = super(SubmissionDetailView, self).get_context_data(**kwargs)
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
        self.object = form.save(commit=False)
        self.object.problem = self.problem
        self.object.user = self.request.user
        print self.object.code
        self.object.save()
        print 'language: ', self.object.language
        try:
            req = {
                'grader': 'custom',
                'submission_id': self.object.id, 
                'problem_id': self.problem.id,
                'source': self.object.code,
                'language': self.object.language,
                'time_limit': self.problem.time_limit,
                'memory_limit': self.problem.memory_limit,
                'problem_data': self.problem.get_problem_data()
            }
            send_to_nsq('judge', json.dumps(req))
        except Exception as ex:
            print ex
        return super(SubmissionCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('submission:submission-list')


