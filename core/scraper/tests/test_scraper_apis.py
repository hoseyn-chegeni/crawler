from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from scraper.models import ScrapedData
from accounts.models import User


class ScrapedDataAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('scraper:api-v1:scraped-data')  
        self.user = User.objects.create_user(email='testuser@test.com', password='testpass')

    def test_authentication_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
