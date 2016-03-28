from rest_framework import serializers
from .models import Problem, ProblemData


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Problem
        #  fields = '__all__'.append('id')
        #  fields = ('url', 'username', 'email', 'is_staff')


class ProblemDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProblemData
        #  fields = '__all__'
