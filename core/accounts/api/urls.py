from django.urls import path, include
from .views import UserListCreateAPIView,UserRetrieveUpdateDestroyAPIView


app_name = "api"

urlpatterns = [
    path('users', UserListCreateAPIView.as_view(), name = 'users'),
    path('user/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name = 'user_single'),
    ]
