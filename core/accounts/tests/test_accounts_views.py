from django.test import TestCase, Client
from ..views import User
from django.urls import reverse


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

    def test_login(self):
        url = reverse("accounts:login")
        login_data = {
            "username": "test@example.com",
            "password": "password123",
        }
        response = self.client.post(url, login_data, follow=True)

        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(response.status_code, 200)
