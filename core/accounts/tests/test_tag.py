from django.test import TestCase
from django.contrib.auth import get_user_model
from recipe.models import Tag

def create_user(email='test@example.com',password='test@1345'):
    return get_user_model().objects.create_user(email=email,password=password)
class CreateTagTests(TestCase):

    def test_create_tag(self):
        user=create_user()
        tag=Tag.objects.create(user=user,name='vegan')

        self.assertEqual(str(tag),tag.name)

