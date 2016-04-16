from rest_framework import serializers
from django.contrib.auth.models import User, Group
#  from .models import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', )


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    nickname = serializers.CharField(source='profile.nickname', max_length=30)

    class Meta:
        model = User
        fields = ('url', 'username', 'password', 'nickname', )

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)

        for (k, v) in profile.items():
            setattr(user.profile, k, v)
        user.profile.save()

        return user

    def update(self, instance, validated_data):
        profile = validated_data.pop('profile')
        password = validated_data.pop('password')

        for (k, v) in validated_data.items():
            setattr(instance, k, v)
        instance.set_password(password)
        instance.save()

        for (k, v) in profile.items():
            setattr(instance.profile, k, v)
        instance.profile.save()

        return instance


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name', )


class UserSlugSerializer(serializers.ModelSerializer):
    """
    status = serializers.SerializerMethodField()

    def get_status(self, object):
        return "in group"
    """

    class Meta:
        model = User
        fields = ('username', )


class GroupUsersSerializer(serializers.ModelSerializer):
    user_set = UserSlugSerializer(many=True)

    class Meta:
        model = Group
        fields = ('user_set', )
