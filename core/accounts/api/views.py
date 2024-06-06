from .serializers import UserUpdateSerializer, UserCreateSerializer
from ..models import User
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserCreateSerializer
    queryset=  User.objects.all()

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset=  User.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserCreateSerializer