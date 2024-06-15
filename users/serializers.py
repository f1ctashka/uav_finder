from rest_framework import serializers
from users.models import User


class RegisterUserInputSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()


class ResetPasswordInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()


class UserUpdateInputSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, allow_blank=True)
    last_name = serializers.CharField(max_length=150, allow_blank=True)
    username = serializers.CharField(
        max_length=150, validators=[User.username_validator]
    )
    birth_date = serializers.DateField()
    gender = serializers.ChoiceField(choices=User.Gender.choices)
    phone_number = serializers.CharField(max_length=20, allow_blank=True)
    address = serializers.CharField(max_length=255, allow_blank=True)
    is_staff = serializers.BooleanField(required=False)  # only admin can change this


class UserOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    is_staff = serializers.BooleanField()
    email = serializers.CharField()
    gender = serializers.CharField()
    birth_date = serializers.DateField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
