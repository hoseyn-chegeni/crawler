from .serializers import ScrapedDataSerializer
from ...models import ScrapedData
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class ScrapedDataListView(ListAPIView):
    serializer_class = ScrapedDataSerializer
    queryset = ScrapedData.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = [
        "id",
        "title",
        "employment_type",
        "location",
        "gender",
        "salary",
        "skills",
        "job_classification",
        "military_service_status",
        "company_name",
        "web_app",
    ]
    ordering_fields = ["id", "created_at"]
