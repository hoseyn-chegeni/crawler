from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
    )
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
