from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
import django.contrib.auth.password_validation as validators


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "confirm_password")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
            }
        }

    def validate(self, attrs):

        if attrs["password"] != attrs["confirm_password"]:
            raise ValueError("password dont match!")
        errors = {}
        try:
            validators.validate_password(
                password=attrs["password"], user=attrs["email"]
            )

        except serializers.ValidationError as e:
            errors["password"] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        """
        Create and return a new user.
        """
        validated_data.pop("confirm_password")
        user = get_user_model().objects.create_user(**validated_data)
        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer for user authentication token.
    """

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user.
        """

        email = attrs["email"]
        password = attrs["password"]
        request=self.context.get("request")
        user = authenticate(request=request, email=email, password=password)
        if not user:
            raise serializers.ValidationError("user dosent exist!")
        attrs["user"] = user
        return attrs
