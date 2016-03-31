from rest_framework import serializers
from .models import Problem, ProblemData, Language, Submission
from filer.models.filemodels import File


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['url', 'file', ]


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem


class ProblemDataSerializer(serializers.HyperlinkedModelSerializer):
    data = FileSerializer()

    class Meta:
        model = ProblemData


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Submission
