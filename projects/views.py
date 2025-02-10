from django.shortcuts import render, redirect
from django.urls.exceptions import NoReverseMatch

from .models import Project
from .forms import ProjectForm
from estimation.models import Contract


def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:panel")
    else:
        form = ProjectForm()
    return render(request, 'projects/create_project.html', context={'form': form})


def edit_project(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == "POST":
        form = ProjectForm(instance=project, data=request.POST)
        if form.is_valid():
            form.save()
            try:
                return redirect("project:get_project", project_id=project.id)
            except NoReverseMatch:
                return redirect("users:panel")
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/edit_project.html', context={'form': form, 'project': project})
    

def get_project(request, project_id):
    project = Project.objects.get(id=project_id)
    contracts = Contract.objects.filter(shot_subject_contract=project).order_by("customer", "date_signing").all()
    context = {'project': project, 'employees': project.get_employees, 'contracts': contracts}
    return render(request, "projects/project.html", context)
