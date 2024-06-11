from django.urls import path
from .views import (
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    RegistrationAPiView,
    CustomObtainAuthToken,
    CustomDiscardAuthToken,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name = "api"

urlpatterns = [
    path("users/", UserListCreateAPIView.as_view(), name="users"),
    path("registration/", RegistrationAPiView.as_view(), name="registration"),
    path(
        "users/<int:pk>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user_single",
    ),
    path("token/login/", CustomObtainAuthToken.as_view(), name="token_login"),
    path("token/logout/", CustomDiscardAuthToken.as_view(), name="token_logout"),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
]
