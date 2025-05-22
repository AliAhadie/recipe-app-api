from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from decimal import Decimal
from recipe.models import Recipe, Tag
from recipe.api.v1.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    Tagserializer,
)
from django.urls import reverse
from rest_framework import status

RECIPE_URL = reverse("recipe:recipe-list")


def get_detail_url(recipe_id):
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(user, **kwargs):
    default = {
        "title": "sample recipe title",
        "time_minutes": 22,
        "price": Decimal("5.2"),
        "description": "this is a sample description",
        "link": "https//example.com/recipe.pdf",
    }
    default.update(**kwargs)
    recipe = Recipe.objects.create(user=user, **default)
    return recipe


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class RecipePublicTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class RecipePrivateTest(TestCase):

    def setUp(self):
        """Set up the user and client for testing"""
        self.client = APIClient()
        self.user = create_user(email="test@example.com", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_retrieve_recipes(self):
        """Test retrieving recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limit(self):
        """Test that the user can only retrieve their own recipes"""
        other_user = create_user(email="other@example.com", password="testpass")

        create_recipe(user=self.user)
        create_recipe(user=other_user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_detail(self):
        """Test retrieving a recipe detail"""
        recipe = create_recipe(user=self.user)
        url = get_detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            "title": "New Recipe",
            "time_minutes": 30,
            "price": Decimal("10.00"),
            "description": "A new recipe description",
            "link": "https://example.com/new-recipe.pdf",
        }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))


    def test_fully_update_recipe(self):
        """Test fully updating a recipe"""
        recipe = create_recipe(
            user=self.user,
            title="Original Recipe Title",
            time_minutes=30,
            price=Decimal("10.00"),
            description="Original recipe description",
            link="https://example.com/original-recipe.pdf",
        )
        payload = {
            "title": "Updated Recipe Title",
            "time_minutes": 25,
            "price": Decimal("12.00"),
            "description": "Updated recipe description",
            "link": "https://example.com/updated-recipe.pdf",
        }
        url = get_detail_url(recipe.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()

        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe"""
        recipe = create_recipe(user=self.user)
        url = get_detail_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_recipe_not_found(self):
        """Test retrieving a non-existent recipe"""
        url = get_detail_url(999)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recipe_with_new_tag(self):
        """Test creating a recipe with new tags"""
        payload = {
            "title": "New Recipe",
            "time_minutes": 30,
            "price": Decimal("10.00"),
            "description": "A new recipe description",
            "link": "https://example.com/new-recipe.pdf",
            "tags": [
                {"name": "Dessert"},
                {"name": "Breakfast"},
            ],
        }
        res = self.client.post(RECIPE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)
        for tag in payload['tags']:
            exists = Tag.objects.filter(name=tag['name'], user=self.user).exists()
            self.assertTrue(exists)

    def test_create_recipe_with_existing_tag(self):
        """Test creating a recipe with an existing tag"""
        tag_dessert = Tag.objects.create(name="Dessert", user=self.user)
        payload = {
            "title": "New Recipe",
            "time_minutes": 30,
            "price": Decimal("10.00"),
            "description": "A new recipe description",
            "link": "https://example.com/new-recipe.pdf",
            "tags": [
                {
                    "name": "Dessert",
                },
                {"name": "Breakfast"},
            ],
        }
        res = self.client.post(RECIPE_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipes = Recipe.objects.filter(user=self.user)
        self.assertEqual(recipes.count(), 1)
        recipe = recipes[0]
        self.assertEqual(recipe.tags.count(), 2)
        self.assertIn(tag_dessert, recipe.tags.all())
        for tag in payload['tags']:
            exists = Tag.objects.filter(name=tag['name'], user=self.user).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self):
        """test create tag while update recipe"""
        recipe=create_recipe(user=self.user)
        payload={
            'tags':[{'name':'dinner'}]
        }
        url=get_detail_url(recipe.id)
        res=self.client.patch(url,payload,format='json')
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        new_tag=Tag.objects.get(user=self.user,name='dinner')
        self.assertIn(new_tag,recipe.tags.all())

    def test_update_assign_tag(self):
        tag_brakfast=Tag.objects.create(user=self.user,name='brakfast')
        recipe=create_recipe(user=self.user)
        recipe.tags.add(tag_brakfast)

        tag_lunch=Tag.objects.create(user=self.user,name='lunch')
        payload={
            'tags':[{'name':'lunch'}]
        }
        url=get_detail_url(recipe.id)
        res=self.client.patch(url,payload,format='json')
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn(tag_lunch,recipe.tags.all())
        self.assertNotIn(tag_brakfast,recipe.tags.all())

    def test_clear_tag(self):
        recipe = create_recipe(user=self.user)
        tag = Tag.objects.create(user=self.user, name='dinner')
        recipe.tags.add(tag)

        payload = {
            'tags': []
        }

        url = get_detail_url(recipe.id)
        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.tags.count(), 0)