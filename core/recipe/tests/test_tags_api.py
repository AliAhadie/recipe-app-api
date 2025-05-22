from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from recipe.models import Tag
from recipe.api.v1 import serializers
from django.urls import reverse



TAGS_URL = reverse("recipe:tag-list")
def get_detail_url(tag_id):
    return reverse('recipe:tag-detail',args=[tag_id])


def create_user(email="test@example.com", password="test@1234"):
    return get_user_model().objects.create_user(email=email, password=password)


class TagsPublicApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class TagsPrivateApiTests(TestCase):

    def setUp(self):
        self.user=create_user()
        self.client=APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tag(self):
        Tag.objects.create(user=self.user,name='spageti')
        Tag.objects.create(user=self.user,name='nodel')

        tags=Tag.objects.all()
        serializer=serializers.Tagserializer(tags,many=True)
        res=self.client.get(TAGS_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_tag_limited_user(self):
        user2=create_user(email='test2@email.com',password='2002ALi')
        Tag.objects.create(user=user2,name='beef')
        tag=Tag.objects.create(user=self.user,name='salad')
        
        res=self.client.get(TAGS_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],tag.name)
        self.assertEqual(res.data[0]['id'],tag.id)

    def test_update_tag(self):
        """test for upadate tag. """
        tag=Tag.objects.create(user=self.user,name='lucnch')   
        url=get_detail_url(tag.id)
        payload={
            'name':'dinner'
        }
        res=self.client.patch(url,payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name,payload['name'])

    def test_delete_tag(self):
        tag=Tag.objects.create(user=self.user)
        url=get_detail_url(tag.id)
        res=self.client.delete(url)

        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)
        tags=Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())    