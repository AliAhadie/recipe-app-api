from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from decimal import Decimal
from recipe.models import Recipe
from recipe.api.v1.seriaizers import RecipeSerializer 
from django.urls import reverse
from rest_framework import status

RECIPE_URL=reverse('recipe:recipe-list')

def create_recipe(user,**kwargs):
    default={
        'title':'sample recipe title',
        'time_minutes':22,
        'price':Decimal('5.2'),
        'description':'this is a sample description',
        'link':'https//example.com/recipe.pdf'
    }
    default.update(**kwargs)
    recipe=Recipe.objects.create(user=user,**default)
    return recipe

class RecipePublicTest(TestCase):

    def setUp(self):
        self.client=APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res=self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class RecipePrivateTest(TestCase):

    def setUp(self):
        """Set up the user and client for testing"""
        self.client=APIClient()
        self.user=get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        """Test retrieving recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res=self.client.get(RECIPE_URL)

        recipes=Recipe.objects.all().order_by('-id')
        serializer=RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_recipe_limit(self):
        """Test that the user can only retrieve their own recipes"""
        other_user=get_user_model().objects.create_user(
            email='other@example.com',
            password='testpass'
        )
        
        create_recipe(user=self.user)
        create_recipe(user=other_user)
        res=self.client.get(RECIPE_URL)
        recipes=Recipe.objects.filter(user=self.user)
        serializer=RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)  
        self.assertEqual(res.data,serializer.data)