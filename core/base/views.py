from django.shortcuts import  HttpResponseRedirect
from django.views.generic import DeleteView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django_filters.views import FilterView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


# Create your views here.
class BaseListView(LoginRequiredMixin, PermissionRequiredMixin, FilterView):
    def get_paginate_by(self, queryset):
        # Get the value for paginate_by dynamically (e.g., from a form input or session)
        # Example: Set paginate_by to a user-selected value stored in session
        user_selected_value = self.request.session.get(
            "items_per_page", 10
        )  # Default to 10
        return user_selected_value

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-created_at")


class BaseCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    success_message = ""
    app_name = ""
    url_name = ""

    def get_success_url(self):
        return reverse_lazy(
            f"{self.app_name}:{self.url_name}", kwargs={"pk": self.object.pk}
        )

    def get_success_message(self, cleaned_data):
        return "با موفقیت افزوده شد"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BaseDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    pass


class BaseUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    app_name = ""
    url_name = ""

    def get_success_url(self):
        return reverse_lazy(
            f"{self.app_name}:{self.url_name}", kwargs={"pk": self.object.pk}
        )

    def get_success_message(self, cleaned_data):
        return "با موفقیت ویرایش شد"


class BaseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    message = "با موفقیت از سیستم حذف شد"
    app_name = ""
    url_name = ""

    def get(self, request, *args, **kwargs):
        # Get the object to be deleted
        self.object = self.get_object()

        # Perform the delete operation directly without displaying a confirmation template

        self.object.delete()
        messages.success(self.request, self.message)
        return HttpResponseRedirect(reverse_lazy(f"{self.app_name}:{self.url_name}"))
