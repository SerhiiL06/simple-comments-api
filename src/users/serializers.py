from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, source="password")
    password2 = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def validate(self, attrs):
        if attrs.get("password1") != attrs.get("password2"):
            raise ValidationError("Passwords must be the same")
        return super().validate(attrs)
