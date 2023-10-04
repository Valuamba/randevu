
from rest_framework import serializers

from apps.users.models import User


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pkid'
        ]


class OwnerCreateSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, required=True)
    sub_domain = serializers.CharField(max_length=30, required=True)
    login = serializers.EmailField(required=True)


class OwnerAccountVerifySerializer(serializers.Serializer):
    code = serializers.IntegerField()
    login = serializers.EmailField(required=True)


class UserJWTSerializer(serializers.Serializer):
    jwt = serializers.CharField()
    refresh = serializers.CharField(required=False)
    pkid = serializers.IntegerField()
    role = serializers.IntegerField()


class UserRecoveryCodeSerializer(serializers.Serializer):
    login = serializers.CharField()


class UserRecoveryVerifyCodeSerializer(serializers.Serializer):
    code = serializers.IntegerField()


class NewUserPasswordSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()


class UserSiginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class RefreshJWTSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()