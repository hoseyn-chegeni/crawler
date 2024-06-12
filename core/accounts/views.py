from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.


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
