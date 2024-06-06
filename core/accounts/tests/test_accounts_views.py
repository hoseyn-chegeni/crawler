from django.test import TestCase, Client,RequestFactory
from ..views import User
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from accounts.views import UserListView
from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

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



class UserListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='12345', is_superuser = True)
        self.user_2 = User.objects.create_user(email='testuser2@example.com', password='12345')
        self.user_with_permission = User.objects.create_user(email='permitteduser@example.com', password='12345')
        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.get(codename='view_user', content_type=content_type)
        self.user_with_permission.user_permissions.add(permission)
        for i in range(15):
            User.objects.create_user(email=f'user{i}@example.com', password='12345')

    def test_pagination(self):
        self.client.login(email='testuser@example.com', password='12345')
        session = self.client.session
        session['items_per_page'] = 10
        session.save()
        response = self.client.get(reverse('accounts:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['users']), 10)

    def test_queryset_ordering(self):
        self.client.login(email='testuser@example.com', password='12345')
        response = self.client.get(reverse('accounts:list'))
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        self.assertTrue(users.ordered)
        self.assertEqual(users.query.order_by, ('-created_at',))

    def test_filtering(self):
        self.client.login(email='testuser@example.com', password='12345')
        response = self.client.get(reverse('accounts:list'), {'email': 'user1@example.com'})
        self.assertEqual(response.status_code, 200)
        users = response.context['users']
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, 'user1@example.com')

    def test_permission_denied(self):
        self.client.login(email='testuser2@example.com', password='12345')
        response = self.client.get(reverse('accounts:list'))
        self.assertEqual(response.status_code, 403)
