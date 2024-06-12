from django.urls import path, include
from .views import (
    logout_view,
    LoginView,
)

app_name = "accounts"

urlpatterns = [
    path("api/v1/", include("accounts.api.v1.urls")),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
