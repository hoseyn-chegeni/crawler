from django.urls import reverse, resolve
from django.test import TestCase
from accounts.views import (
    UserListView, UserCreateView, UserDetailView, 
    UserUpdateView, UserDeleteView, LoginView, logout_view
)
from django.contrib.auth import get_user_model


class TestAccountsUrls(TestCase):

    def setUp(self):
        self.url_names = [
            ('list', UserListView),
            ('create', UserCreateView),
            ('detail', UserDetailView),
            ('update', UserUpdateView),
            ('delete', UserDeleteView),
            ('login', LoginView),
        ]
        self.urls = [
            ('accounts:list', {}, 'get'),
            ('accounts:create', {}, 'get'),
            ('accounts:detail', {'pk': 1}, 'get'),
            ('accounts:update', {'pk': 1}, 'get'),
            ('accounts:delete', {'pk': 1}, 'get'),
            ('accounts:login', {}, 'get'),
            ('accounts:logout', {}, 'get'),
        ]
        self.dict_urls = [
            'accounts:list',
            'accounts:create',
        ]

        User = get_user_model()
        self.user = User.objects.create_user(email='test@test.com', password='testpassword')


    def test_accounts_urls_resolve(self):
        for url_name, expected_view in self.url_names:
            with self.subTest(url_name=url_name):
                if url_name in ['detail', 'update', 'delete']:
                    url = reverse(f'accounts:{url_name}', kwargs={'pk': 1})
                else:
                    url = reverse(f'accounts:{url_name}')
                
                resolved = resolve(url)
                self.assertEqual(resolved.func.view_class, expected_view)

    def test_accounts_urls_status(self):
        self.client.login(username='testuser', password='testpassword')
        
        for url_name, kwargs, method in self.urls:
            with self.subTest(url_name=url_name):
                url = reverse(url_name, kwargs=kwargs if kwargs else None)
                response = getattr(self.client, method)(url)
                self.assertIn(response.status_code, range(200, 399), f"URL {url} returned status code {response.status_code}")

    def test_unauthenticated_access_redirect(self):
        for url_name in self.dict_urls:
            url = reverse(url_name)
            response = self.client.get(url)
            self.assertRedirects(response, f'/accounts/login/?next={url}', fetch_redirect_response=False)

