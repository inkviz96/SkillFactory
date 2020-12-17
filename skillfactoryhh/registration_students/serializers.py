from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        min_length=2,
        max_length=128,
        required=True,
    )

    last_name = serializers.CharField(
        min_length=2,
        max_length=128,
        required=True,
    )

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    password = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
        ]

    def create(self, validated_data):
        return User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
