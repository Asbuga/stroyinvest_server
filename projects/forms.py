from django import forms

from .models import Project
from users.models import Employee


class ProjectForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(),
        label="Найменування проекту",
    )
    manager = forms.ModelChoiceField(
        queryset=Employee.objects.filter(department__title__icontains="Менеджер"),
        label="Менеджер",
        required=False,
    )
    engineer = forms.ModelChoiceField(
        queryset=Employee.objects.filter(department__title__icontains="(ПТО)"),
        label="Інженер ВТВ",
        required=False,
    )
    foreman = forms.ModelChoiceField(
        queryset=Employee.objects.filter(department__title__icontains="Прораб"),
        label="Прораб",
        required=False,
    )
    estimator = forms.ModelChoiceField(
        queryset=Employee.objects.filter(department__title__icontains="Кошторис"),
        label="Кошторисник",
        required=False,
    )
    supply = forms.ModelChoiceField(
        queryset=Employee.objects.filter(department__title__icontains="Постачання"),
        label="Фахівець з постачання",
        required=False,
    )
    accountant = forms.ModelChoiceField(
        queryset=Employee.objects.filter(department__title__icontains="Бухгалтер"),
        label="Бухгалтер",
        required=False,
    )
    economist = forms.ModelChoiceField(
        queryset=Employee.objects.filter(department__title__icontains="Економіст"),
        label="Економіст",
        required=False,
    )

    class Meta:
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
