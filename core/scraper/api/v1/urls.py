from django.urls import path
from .views import ScrapedDataListView
app_name = 'api-v1'

urlpatterns = [
    path('scraped-data', ScrapedDataListView.as_view(), name='scraped-data')
]