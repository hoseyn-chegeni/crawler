from django.shortcuts import render
from base.views import BaseListView, BaseDetailView, BaseDeleteView, BaseUpdateView,BaseCreateView
from .models import User
from .filters import UserFilter
from .forms import CustomUserForm
# Create your views here.

class UserListView(BaseListView):
    model = User
    template_name = "accounts/list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"

class UserCreateView(BaseCreateView):
    model = User
    form_class = CustomUserForm
    template_name = "accounts/create.html"
    app_name = "accounts"
    url_name = "detail"
    permission_required = "accounts.add_user"


class UserDetailView(BaseDetailView):
    model = User
    template_name = "accounts/detail.html"
    context_object_name = "user"
    permission_required = "accounts.view_user"

class UserUpdateView(BaseUpdateView):
    model = User
    form_class = CustomUserForm
    template_name = "accounts/update.html"
    app_name = "accounts"
    url_name = "detail"
    permission_required = "accounts.change_user"

class UserDeleteView(BaseDeleteView):
    model = User
    app_name = "accounts"
    url_name = "list"
    permission_required = "accounts.delete_user"
    message = "کاربر با موفقیت حذف شد"

