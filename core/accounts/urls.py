from django.urls import path, include
from .views import (
    UserListView,
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserUpdateView,
    logout_view,
    LoginView,
)

app_name = "accounts"

urlpatterns = [
    path("api/", include("accounts.api.urls")),
    path("list/", UserListView.as_view(), name="list"),
    path("create/", UserCreateView.as_view(), name="create"),
    path("detail/<int:pk>/", UserDetailView.as_view(), name="detail"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="delete"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
