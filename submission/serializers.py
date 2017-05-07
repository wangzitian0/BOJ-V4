from rest_framework import serializers
from .models import Submission
from problem.models import Problem


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Submission

