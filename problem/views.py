from rest_framework import viewsets
from .models import Problem, ProblemData
from .serializers import ProblemSerializer, ProblemDataSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ProblemDataViewSet(viewsets.ModelViewSet):
    queryset = ProblemData.objects.all()
    serializer_class = ProblemDataSerializer
