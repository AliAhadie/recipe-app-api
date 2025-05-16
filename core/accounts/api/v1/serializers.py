from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
import django.contrib.auth.password_validation as validators


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """

    class Meta:
        model = get_user_model()
        fields = ("email", "password")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
            }
        }


    def create(self, validated_data):
        """
        Create and return a new user.
        """
        
        user = get_user_model().objects.create_user(**validated_data)
        return user
    
    
    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

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



