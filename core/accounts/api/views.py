from .serializers import UserUpdateSerializer, UserCreateSerializer
from ..models import User
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .paginations import LargeResultsSetPagination


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserCreateSerializer
    queryset=  User.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["id",'email','is_superuser']
    ordering_fields = ['id', 'created_at']
    pagination_class = LargeResultsSetPagination

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset=  User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserCreateSerializer