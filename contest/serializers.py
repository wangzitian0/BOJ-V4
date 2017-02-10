from rest_framework import serializers
from rest_framework.renderers import JSONRenderer


class UserSerializer(serializers.Serializer):

    user_pk = serializers.IntegerField()
    user_name = serializers.CharField(max_length=30)
    contest_pk = serializers.IntegerField()
    cost_time = serializers.DurationField()
    all_sub = serializers.IntegerField()
    problem_ac = serializers.DictField(child=serializers.IntegerField())
    problem_time = serializers.DictField(child=serializers.DurationField())
    problem_sub = serializers.DictField(child=serializers.IntegerField()) 

    def toJson(self):
        return JSONRenderer().render(self.data)

