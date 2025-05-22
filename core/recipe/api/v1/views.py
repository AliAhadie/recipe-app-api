from rest_framework import viewsets,mixins
from recipe.api.v1.serializers import (RecipeSerializer, 
                                       RecipeDetailSerializer,Tagserializer)
from recipe.models import (Recipe,Tag)
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

class TagApiViewSet(viewsets.ModelViewSet):
    serializer_class = Tagserializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
