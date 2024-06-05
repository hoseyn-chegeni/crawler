from django.urls import path
from .views import UserListView
app_name = 'accounts'

urlpatterns = [
    path('list/', UserListView.as_view(), name = 'list'),
]