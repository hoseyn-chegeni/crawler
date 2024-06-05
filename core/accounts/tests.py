from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'first_name': 'Test',
            'last_name': 'User',
            'is_superuser' : True
        }
        self.user = User.objects.create_user(**self.user_data)
        self.login_data = {
            'username': self.user.email,
            'password': 'testpassword123'
        }
        self.update_data = {
            'first_name': 'Updated',
            'last_name': 'User'
        }
        self.client.login(username=self.user.email, password='testpassword123')

    def test_user_list_view(self):
        response = self.client.get(reverse('accounts:list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user.email)

    def test_user_create_view(self):
        new_user_data = {
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(reverse('accounts:create'), new_user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_view(self):
        response = self.client.get(reverse('accounts:detail', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.user.email)

    def test_user_update_view(self):
        response = self.client.post(reverse('accounts:update', kwargs={'pk': self.user.pk}), self.update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')

    def test_user_delete_view(self):
        response = self.client.post(reverse('accounts:delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_login_view(self):
        response = self.client.post(reverse('accounts:login'), self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)

    def test_logout_view(self):
        self.client.login(username=self.user.email, password='testpassword123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Redirect after logout
        self.assertRedirects(response, reverse('accounts:login'))

    def test_create_user_with_existing_email(self):
        response = self.client.post(reverse('accounts:create'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_wrong_password(self):
        wrong_login_data = self.login_data.copy()
        wrong_login_data['password'] = 'wrongpassword'
        response = self.client.post(reverse('accounts:login'), wrong_login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
