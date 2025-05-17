from rest_framework import viewsets
from recipe.api.v1.serializers import RecipeSerializer
from recipe.models import Recipe
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions  import IsAuthenticated
class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class=RecipeSerializer
    queryset=Recipe.objects.all()
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)