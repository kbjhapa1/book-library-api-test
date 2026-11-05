from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Book

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    # Show the owner's username; clients can never set it themselves.
    owner = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "author", "published_year", "owner", "created_at"]
        read_only_fields = ["id", "owner", "created_at"]

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be blank.")
        return value

    def validate_author(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Author cannot be blank.")
        return value

    def validate_published_year(self, value):
        if value is not None and not (1000 <= value <= 2100):
            raise serializers.ValidationError("Year must be between 1000 and 2100.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=[UnicodeUsernameValidator()])
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate(self, attrs):
        # Reuse Django's password rules (length, common passwords, ...).
        try:
            validate_password(attrs["password"], user=User(username=attrs["username"]))
        except DjangoValidationError as exc:
            raise serializers.ValidationError({"password": list(exc.messages)})
        return attrs

    def create(self, validated_data):
        # create_user() hashes the password. We never store the plain text.
        return User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)