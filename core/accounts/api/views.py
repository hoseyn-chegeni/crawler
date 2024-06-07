from .serializers import UserSerializer, RegistrationSerializer
from ..models import User
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .pagination import LargeResultsSetPagination
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status



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


class RegistrationAPiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'email': serializer.validated_data['email']
            }
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

