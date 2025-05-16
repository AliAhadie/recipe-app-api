from rest_framework.generics import CreateAPIView
from accounts.api.v1.serializers import CreateUserSerializer


class UserCreateApiView(CreateAPIView):
    """
    View for creating a new user.
    """
    serializer_class = CreateUserSerializer

    