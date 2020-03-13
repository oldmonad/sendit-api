from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from sendit.apps.profiles.serializers import ProfileSerializer

from .models import User


class PasswordSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.RegexField(
        regex=("^(?=.{8,}$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*"),
        min_length=8,
        max_length=30,
        required=True,
        write_only=True,
        error_messages={
            "required": "Password is a required field",
            "min_length": "Password must be at least 8 characters long",
            "max_length": "Password cannot be more than 30 characters",
            "invalid": "Password must have at least a number, and a least an uppercase and a lowercase letter",
        },
    )

    confirm_password = serializers.CharField(
        max_length=30, min_length=8, required=False
    )


class RegistrationSerializer(PasswordSerializer, serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Email is already in use by another user",
            )
        ],
        error_messages={
            "invalid": "Email must be of the format name@domain.com",
            "required": "Email is a required field",
        },
    )

    full_name = serializers.CharField(
        required=True,
        error_messages={"required": "Full name is a required property",},  # noqa
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "password", "token")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    full_name = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        if email is None:
            raise serializers.ValidationError("An email address is required to log in.")
        if password is None:
            raise serializers.ValidationError("A password is required to log in.")
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found."
            )
        if not user.is_active:
            raise serializers.ValidationError("This user has been deactivated.")
        return {"email": user.email, "full_name": user.full_name, "token": user.token}

        return instance  # noqa


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    profile = ProfileSerializer(read_only=True)

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "password", "profile")

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop("password", None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
