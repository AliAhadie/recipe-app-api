from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("accounts:create")
CREATE_TOKEN_URL = reverse("accounts:token")
ME_URL = reverse("accounts:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserPublicTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "confirm_password": "testpass123",
        }

        res = self.client.post(CREATE_USER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exists(self):
        """Test error returned if user exists"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
            "confirm_password": "testpass123",
        }
        data.pop("confirm_password")
        create_user(**data)
        res = self.client.post(CREATE_USER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.filter(email=data["email"]).exists()
        self.assertTrue(user)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        data = {
            "email": "test@example.com",
            "password": "testpass123",
        }
        create_user(**data)
        res = self.client.post(CREATE_TOKEN_URL, data)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email="test@example.com", password="testpass123")
        data = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }
        res = self.client.post(CREATE_TOKEN_URL, data)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_unauthorized(self):
        """Test that user is unauthorized if not logged in"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UserPrivateTests(TestCase):

    def setUp(self):
        """
        Set up the user for testing.
        """
        self.client = APIClient()

        self.user = {"email": "test@example.com", "password": "testpass1234"}
        self.client.force_authenticate(self.user)

    def test_get_me_view(self):
        """
        Test retrieving the current user profile.
        """

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], self.user.email)

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me endpoint"""
        res = self.client.post(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test updating the user profile for authenticated users.
        """

        data = {"password": "newpassword123"}
        res = self.client.patch(ME_URL, data)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(data["password"]))
