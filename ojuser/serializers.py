from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import GroupProfile
#  from .models import UserProfile

def get_rand_password():
    import random
    numbers = '1234567890abcdefghijklmn'
    return ''.join([random.choice(numbers) for i in range(6)])

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', )


class UserSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class UserResetSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    password = serializers.CharField(max_length=20)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    user_set = UserSlugSerializer(many=True)

    class Meta:
        model = Group
        fields = ('url', 'name', 'user_set')


class GroupProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_group = GroupSerializer()
    admin_group = GroupSerializer()

    class Meta:
        model = GroupProfile
        fields = ('url', 'name', 'nickname', 'user_group', 'admin_group', )


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    nickname = serializers.CharField(source='profile.nickname', max_length=30)

    class Meta:
        model = User
        fields = ('url', 'username', 'password', 'nickname')

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        print 'password============', validated_data['password']
        # self.new_pwd = validated_data['password']
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
