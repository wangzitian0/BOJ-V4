from rest_framework import serializers
from .models import Problem, ProblemData


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem


class ProblemDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProblemData
