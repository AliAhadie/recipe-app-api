from rest_framework.generics import CreateAPIView,UpdateAPIView,GenericAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from accounts.api.v1.serializers import (CreateUserSerializer,
                                         AuthTokenSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework.views import Response
from rest_framework import status

class UserCreateApiView(CreateAPIView):
    """
    View for creating a new user.
    """
    serializer_class = CreateUserSerializer

class AuthTokenApiView(ObtainAuthToken):
    """
    View for creating a new auth token.
    """
    serializer_class = AuthTokenSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES

class UpdateUserApiView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    serializer_class = CreateUserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
