from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


from projects.models import Project

from .models import Department
from .forms import CustomAuthenticationForm, UserEmployeeForm, DepartmentForm


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy("estimation:get_acts")


def register(request):
    """Registers a new user."""
    if request.method == "POST":
        form = UserEmployeeForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:panel")
    else:
        form = UserEmployeeForm()
    context = {"form": form}
    return render(request, "users/register.html", context)


def panel(request):
    """Employee panel."""
    return redirect("estimation:get_acts")
    """
    projects = Project.objects.get_estimator_projects(request.user.id)
    context = {"projects": projects}
    return render(request, "users/panel.html", context)
    """
    

def home_page(request):
    pass


# Work with departments.
def get_departments(request):
    title = "Відділи"
    departments = Department.objects.order_by("title").all()
    context = {"departments": departments, "title": title}
    return render(request, "users/department/departments.html", context)


def get_department(request, department_id):
    department = Department.objects.get(id=department_id)
    context = {"departments": department, "title": department.title}
    return render(request, "users/department/get_department.html", context)

def add_department(request):
    if request.method == "POST":
        form = DepartmentForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:panel")
    else:
        form = UserEmployeeForm()
    context = {"form": form}
    return render(request, "users/register.html", context)




def edit_department(request):
    pass


def delete_department(request):
    pass


# Work with Employee.
def get_employees(request):
    pass


def add_employee(request):
    pass


def get_employee(request):
    pass


def edit_employee(request):
    pass


def delete_employee(request):
    pass
