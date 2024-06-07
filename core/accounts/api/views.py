from .serializers import UserSerializer, RegistrationSerializer, CustomAuthTokenSerializer
from ..models import User
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .pagination import LargeResultsSetPagination
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView


class UserListCreateAPIView(ListAPIView): 
    permission_classes = [IsAuthenticated]  
    serializer_class = UserSerializer
    queryset=  User.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["id",'email','is_superuser']
    ordering_fields = ['id', 'created_at']
    pagination_class = LargeResultsSetPagination

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]  
    queryset=  User.objects.all()
    serializer_class = UserSerializer


class RegistrationAPiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'email': serializer.validated_data['email']
            }
            return Response(data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class CustomObtainAuthToken (ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

