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

    def test_create_superuser(self):
        email='admin@example.com'
        password='test@1234'
        user=get_user_model().objects.create_superuser(email=email,password=password)
        self.assertTrue(user.is_superuser) 
        self.assertTrue(user.is_staff) 


            