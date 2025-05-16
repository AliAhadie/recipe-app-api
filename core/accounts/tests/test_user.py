from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL =reverse('accounts:create')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful"""
        data={
            'email': 'test@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        }   

        res=self.client.post(CREATE_USER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user=get_user_model().objects.get(email=data['email'])
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test error returned if user exists"""
        data={
            'email': 'test@example.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        } 
        data.pop('confirm_password')
        create_user(**data)
        res=self.client.post(CREATE_USER_URL, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user=get_user_model().objects.filter(email=data['email']).exists()
        self.assertTrue(user)
          
        
