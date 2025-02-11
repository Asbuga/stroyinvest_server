"""
URL configuration for stroyinvest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path

from . import views

app_name = "users"
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("register/", views.register, name="register"),
    # Employee panel.
    path("panel/", views.panel, name="panel"),
    # Work with departments.
    path("departments/", views.get_departments, name="get_departments"),
    path("department/add/", views.add_department, name="add_department"),
    path("department/get/<int:department_id>", views.get_department, name="get_department"),
    path("department/edit/<int:department_id>", views.edit_department, name="edit_department"),
    path("department/delete/<int:department_id>", views.delete_department, name="delete_department"),
    # Work with Employee.
    path("employees/", views.get_employees, name="get_employees"),
    path("employee/add/", views.add_employee, name="add_employee"),
    path("employee/get/<int:employee_id>", views.get_employee, name="add_employee"),
    path("employee/edit/<int:employee_id>", views.edit_employee, name="edit_employee"),
    path("employee/delete/<int:employee_id>", views.delete_employee, name="edit_employee"),
]
