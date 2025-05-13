from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Tests for the Django admin modifications."""

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="test@1234"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="userpass123"
        )

    def test_user_list(self):
        """Test that users are listed on user page"""
        url = reverse(
            "admin:accounts_user_changelist"
        )  
        res = self.client.get(url)

        self.assertContains(res, self.user.email)

    def test_add_user_page(self):
        """test user page."""
        url = reverse("admin:accounts_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_edit_user_page(self):
        """test for edit user page."""
        url = reverse("admin:accounts_user_change", args=[self.user.id])
        res=self.client.get(url)
        self.assertEqual(res.status_code,200)
