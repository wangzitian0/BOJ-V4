from rest_framework import viewsets
from .models import Problem, ProblemData
from .serializers import ProblemSerializer, ProblemDataSerializer
from django.views.generic.list import ListView
from rest_framework.permissions import IsAuthenticated


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
