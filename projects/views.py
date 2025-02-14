from django.shortcuts import render
from django.urls import reverse_lazy

from stroyinvest.models import BaseFormView

from .forms import ProjectForm
from .models import Project


EDIT_FORM = "stroyinvest/edit_form.html"


class ProjectFormView(BaseFormView):
    model = Project
    form_class = ProjectForm
    template_name = EDIT_FORM
    success_url = "projects:get_projects"
    title_add = "Додати проект"
    title_edit = "Редагувати проект"


def get_projects(request):
    title = "Проекти"
    projects = Project.objects.all()
    context = {"projects": projects, "title": title}
    return render(request, "projects/projects.html", context)
