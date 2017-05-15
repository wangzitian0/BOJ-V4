from rest_framework import serializers
from .models import Problem, ProblemDataInfo, ProblemCase
from filer.models.filemodels import File


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['url', 'name', 'size', 'file', ]


class ProblemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Problem


class ProblemDataInfoSerializer(serializers.HyperlinkedModelSerializer):
    data = FileSerializer()

    class Meta:
        model = ProblemDataInfo


class ProblemDataSerializer(serializers.HyperlinkedModelSerializer):
    datainfo = ProblemDataInfoSerializer(many=True)

    class Meta:
        model = Problem


class ProblemCaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProblemCase
        fields = ['score', ]

