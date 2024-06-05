from django.shortcuts import render, redirect
from base.views import (
    BaseListView,
    BaseDetailView,
    BaseDeleteView,
    BaseUpdateView,
    BaseCreateView,
)
from .models import User
from .filters import UserFilter
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


class UserListView(BaseListView):
    model = User
    template_name = "accounts/list.html"
    context_object_name = "users"
    filterset_class = UserFilter
    permission_required = "accounts.view_user"


class UserCreateView(BaseCreateView):
    model = User
    form_class = CustomUserCreationForm
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
    form_class = CustomUserUpdateForm
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


def logout_view(request):
    logout(request)
    # Redirect to a desired URL after logout
    return redirect(
        "accounts:login"
    )  # Replace 'login' with the name of your login URL pattern


class LoginView(BaseLoginView):
    template_name = "accounts/login.html"

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse("index:index")
