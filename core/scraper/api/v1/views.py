from .serializers import ScrapedDataSerializer
from ...models import ScrapedData
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import LargeResultsSetPagination
from .filters import ScrapedDataFilter
from rest_framework.permissions import IsAuthenticated


class ScrapedDataListView(ListAPIView):
    serializer_class = ScrapedDataSerializer
    permission_classes = [IsAuthenticated]
    queryset = ScrapedData.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ScrapedDataFilter
    ordering_fields = ["id", "created_at", "title"]
    pagination_class = LargeResultsSetPagination
