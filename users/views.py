from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from projects.models import Project

from .forms import CustomAuthenticationForm, UserEmployeeForm


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


def register(request):
    """Registers a new user."""
    if request.method == "POST":
        form = UserEmployeeForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:home")
    else:
        form = UserEmployeeForm()
    context = {"form": form}
    return render(request, "users/register.html", context)


def panel(request):
    projects = Project.objects.get_estimator_projects(request.user.id)
    context = {"projects": projects}
    return render(request, "users/panel.html", context)
