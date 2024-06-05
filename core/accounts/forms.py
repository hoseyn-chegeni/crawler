from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
        )

class CustomUserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )