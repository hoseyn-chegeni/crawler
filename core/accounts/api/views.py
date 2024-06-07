from .serializers import UserSerializer
from ..models import User
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .paginations import LargeResultsSetPagination


class UserListCreateAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset=  User.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["id",'email','is_superuser']
    ordering_fields = ['id', 'created_at']
    pagination_class = LargeResultsSetPagination

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset=  User.objects.all()
    serializer_class = UserSerializer