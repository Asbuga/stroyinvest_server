from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .models import Project
from .forms import ProjectForm


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/add_project.html'
    success_url = 'users/panel.html'
