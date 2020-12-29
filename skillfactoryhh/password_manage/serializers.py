from rest_framework import serializers


class RestoreAccessSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=30)


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30)
    confirm_password = serializers.CharField(max_length=30)
