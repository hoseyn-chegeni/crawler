from django.shortcuts import render
from base.views import BaseListView
from .models import User
from .filters import UserFilter
# Create your views here.

class UserListView(BaseListView):
    model = User
    template_name = "accounts/list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"