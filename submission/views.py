from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Submission
from .serializers import SubmissionSerializer

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from problem.models import Problem
from django.shortcuts import get_object_or_404
from .forms import SubmissionForm
from django_tables2 import RequestConfig
from .tables import SubmissionTable
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
        context = super(SubmissionDetailView, self).get_context_data(**kwargs)
        return context


class SubmissionCreateView(CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name_suffix = '_create_form'

    @method_decorator(login_required)
    def dispatch(self, request, pid=None, *args, **kwargs):
        pid = self.kwargs['pid']
        self.problem = get_object_or_404(Problem.objects.all(), pk=pid)
        return super(SubmissionCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kw = super(SubmissionCreateView, self).get_form_kwargs()
        kw['qs'] = self.problem.allowed_lang.all()
        return kw

    def get_context_data(self, **kwargs):
        context = super(SubmissionCreateView, self).get_context_data(**kwargs)
        context['problem'] = self.problem
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.problem = self.problem
        self.object.user = self.request.user
        return super(SubmissionCreateView, self).form_valid(form)
