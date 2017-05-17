from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import ContestSubmission


class ContestSubmissionSerializer(serializers.HyperlinkedModelSerializer):

    pk = serializers.IntegerField()
    code = serializers.CharField(max_length=30)

    def toJson(self):
        return JSONRenderer().render(self.data)

    class Meta:
        model = ContestSubmission

