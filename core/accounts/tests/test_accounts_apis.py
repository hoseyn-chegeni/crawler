import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User

@pytest.fixture
def common_user():
    user = User.objects.create_user(email = 'test@test.com', password = 'db@sldk;fj', is_superuser = True)
    return user

@pytest.mark.django_db
class TestAccountsAPi:
    client = APIClient()
    def test_accounts_api_get_response_200_status(self):
        url = reverse('accounts:api:users')
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_user_response_unauthorized_401_status(self):
        url = reverse('accounts:api:registration')
        data = {
            'email':'z@z.com',
            'password':'db@sldk;fj',
            'password1':'db@sldk;fj',
        }
        response = self.client.post(url,data)
        assert response.status_code == 401

    def test_create_user_response_201_status(self, common_user):
        url = reverse('accounts:api:registration')
        data = {
            'email':'z@z.com',
            'password':'db@sldk;fj',
            'password1':'db@sldk;fj',
        }
        self.client.force_authenticate(user = common_user)
        response = self.client.post(url,data)
        assert response.status_code == 201