from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from guardian.shortcuts import get_objects_for_user

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy

from .models import Problem, ProblemData, Language, Submission
from filer.models.filemodels import File

from .serializers import ProblemSerializer, ProblemDataSerializer
from .serializers import SubmissionSerializer, LanguageSerializer, FileSerializer


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated,)


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = (IsAuthenticated,)


class ProblemDataViewSet(viewsets.ModelViewSet):
    queryset = ProblemData.objects.all()
    serializer_class = ProblemDataSerializer
    permission_classes = (IsAuthenticated,)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = (IsAuthenticated,)


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (IsAuthenticated,)


class ProblemListView(ListView):

    model = Problem
    paginate_by = 10

    def get_queryset(self):
        return get_objects_for_user(self.request.user, 'problem.view_problem')


class ProblemDetailView(DetailView):

    model = Problem
    template_name = 'problem/problem_detail.html'

    def get_queryset(self):
        return get_objects_for_user(self.request.user, 'problem.view_problem')

    def get_context_data(self, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(**kwargs)
        return context


class ProblemCreateView(CreateView):
    model = Problem
    fields = '__all__'
    template_name_suffix = '_create_form'


class ProblemUpdateView(UpdateView):
    model = Problem
    fields = '__all__'
    template_name_suffix = '_update_form'


class ProblemDeleteView(DeleteView):
    model = Problem
    success_url = reverse_lazy('problem:problem-list')
