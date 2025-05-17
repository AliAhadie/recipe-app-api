from rest_framework import viewsets
from recipe.api.v1.serializers import RecipeSerializer, RecipeDetailSerializer
from recipe.models import Recipe
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return RecipeSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
