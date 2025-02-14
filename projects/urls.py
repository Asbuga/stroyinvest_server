from django.urls import path

from . import views


app_name = "projects"
urlpatterns = [
    path("projects", views.get_projects, name="get_projects"),
    path("project/add/", views.ProjectFormView.as_view(), name="add_project"),
    path("project/edit/<int:id>/", views.ProjectFormView.as_view(), name="edit_project"),
]
