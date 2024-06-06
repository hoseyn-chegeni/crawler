from .serializers import UserSerializer
from ..models import User
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset=  User.objects.all()

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    pass