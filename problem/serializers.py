from rest_framework import serializers
from .models import Problem, ProblemData, Language, Submission


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem


class ProblemDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProblemData


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Submission
