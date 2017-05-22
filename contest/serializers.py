from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from .models import ContestSubmission
from .models import Contest, ContestProblem, Clarification, Notification


class ContestSubmissionSerializer(serializers.HyperlinkedModelSerializer):

    pk = serializers.IntegerField()
    code = serializers.CharField(max_length=30)
    nickname = serializers.CharField(max_length=30)
    score = serializers.IntegerField(default=0)
    ac_sub = serializers.DictField(child=serializers.IntegerField())
    problem_time = serializers.DictField(child=serializers.DurationField())
    problem_sub = serializers.DictField(child=serializers.IntegerField())

    def toJson(self):
        return JSONRenderer().render(self.data)


class ContestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contest

class ContestProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContestProblem

class ClarificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Clarification

class ContestNotificationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Notification
