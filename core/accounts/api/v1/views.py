from rest_framework.generics import CreateAPIView
from accounts.api.v1.serializers import (CreateUserSerializer,
                                         AuthTokenSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


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
    