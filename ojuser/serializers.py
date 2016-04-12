from rest_framework import serializers
from django.contrib.auth.models import User, Group


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name', )


class UserSlugSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', )


class GroupUsersSerializer(serializers.HyperlinkedModelSerializer):
    """
    data = serializers.SlugRelatedField(
        source='user_set',
        many=True,
        read_only=True,
        slug_field='username'
    )
    """
    data = UserSlugSerializer(source='user_set', many=True)

    class Meta:
        model = Group
        fields = ('data',)
