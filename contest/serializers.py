from rest_framework import serializers
from rest_framework.renderers import JSONRenderer


class UserSerializer(serializers.Serializer):

    pk = serializers.IntegerField()
    nickname = serializers.CharField(max_length=30)
    score = serializers.IntegerField(default=0)
    ac_sub = serializers.DictField(child=serializers.IntegerField())
    problem_time = serializers.DictField(child=serializers.DurationField())
    problem_sub = serializers.DictField(child=serializers.IntegerField()) 

    def toJson(self):
        return JSONRenderer().render(self.data)

