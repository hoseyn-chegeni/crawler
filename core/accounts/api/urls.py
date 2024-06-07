from django.urls import path, include
from .views import UserListCreateAPIView,UserRetrieveUpdateDestroyAPIView, RegistrationAPiView


app_name = "api"

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name = 'users'),
    path('registration/', RegistrationAPiView.as_view(), name = 'registration'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name = 'user_single'),
    ]
