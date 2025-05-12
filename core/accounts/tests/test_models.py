from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    """test for user models."""

    def test_create_user(self):
        """ test for crateing user object """
        email = "test@example.com"
        password = "test@1234"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        """test for normalizing email address."""
        simple_email=[
            ['User@example.com','user@example.com'],
            ["user@example.COM",'user@example.com'],
            ['user@EXAMPLE.com','user@example.com'],
            ['user@ExAmPlE.CoM','user@example.com']

        ]
        for email,expected in simple_email:
            user=get_user_model().objects.create_user(email,'test@1234')
            self.assertEqual(user.email,expected)
            