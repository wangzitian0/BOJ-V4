from rest_framework import serializers
from .models import Problem, ProblemDataInfo, Language
from filer.models.filemodels import File


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['url', 'name', 'size', 'file', ]


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem


class ProblemDataInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProblemDataInfo


class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
