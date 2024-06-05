from django.test import TestCase
from ..models import User
from django.contrib.auth import get_user_model
from datetime import datetime


class TestAccountsModel(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertIsNone(user.first_name)
        self.assertIsNone(user.last_name)
        self.assertIsInstance(user.created_at, datetime)
        self.assertIsInstance(user.updated_at, datetime)
        self.assertIsNone(user.created_by)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="admin@example.com", password="admin123"
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_get_full_name(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@example.com",
            password="password123",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(user.get_full_name(), "John Doe")

    def test_str_representation(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.assertEqual(str(user), "test@example.com")

    def test_created_by_null(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.assertIsNone(user.created_by)
