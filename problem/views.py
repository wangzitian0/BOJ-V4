from rest_framework import viewsets
from .models import Problem, ProblemData
from .serializers import ProblemSerializer, ProblemDataSerializer
from django.views.generic import ListView, DetailView
from rest_framework.permissions import IsAuthenticated
from guardian.shortcuts import get_objects_for_user


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    permission_classes = (IsAuthenticated,)


class ProblemDataViewSet(viewsets.ModelViewSet):
    queryset = ProblemData.objects.all()
    serializer_class = ProblemDataSerializer
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
