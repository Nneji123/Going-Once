# serializers.py

from dj_rest_auth.registration.serializers import RegisterSerializer

# serializers.py
from dj_rest_auth.serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    UserDetailsSerializer,
)
from rest_framework import serializers

from .models import User


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        super().get_cleaned_data()

        return {
            "email": self.validated_data.get("email", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
        }

    def save(self, request):
        user = User(
            email=self.cleaned_data["email"],
        )
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)


class CustomUserDetailsSerializer(UserDetailsSerializer):
    """
    Custom user details serializer
    """

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "profile_pic", "bio")


class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    """
    Custom password change serializer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    """
    Custom password reset confirm serializer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)
