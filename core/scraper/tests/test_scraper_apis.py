from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from scraper.models import ScrapedData
from accounts.models import User
from rest_framework.authtoken.models import Token


class ScrapedDataAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("scraper:api-v1:scraped-data")
        self.user = User.objects.create_user(
            email="testuser@test.com", password="testpass"
        )

    def test_authentication_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ScrapedDataAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("scraper:api-v1:scraped-data")
        self.user = User.objects.create_user(
            email="testuser@mail.com", password="testpass"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_retrieve_scraped_data(self):
        ScrapedData.objects.create(title="Test Job 1", description="Description 1")
        ScrapedData.objects.create(title="Test Job 2", description="Description 2")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_scraped_data(self):
        ScrapedData.objects.create(
            title="Test Job 1", description="Description 1", location="Location 1"
        )
        ScrapedData.objects.create(
            title="Test Job 2", description="Description 2", location="Location 2"
        )

        response = self.client.get(self.url, {"location": "Location 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["location"], "Location 1")

    def test_ordering_scraped_data(self):
        ScrapedData.objects.create(title="B Job", description="Description 1")
        ScrapedData.objects.create(title="A Job", description="Description 2")

        response = self.client.get(self.url, {"ordering": "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["title"], "A Job")
        self.assertEqual(response.data["results"][1]["title"], "B Job")

    def test_pagination_scraped_data(self):
        for i in range(25):
            ScrapedData.objects.create(
                title=f"Test Job {i}", description=f"Description {i}"
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)
        self.assertEqual(len(response.data["results"]), 20)
        self.assertTrue("next" in response.data)
