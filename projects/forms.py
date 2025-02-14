from django import forms

from .models import Project
from users.models import Employee


class ProjectForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(),
        label="Найменування проекту",
    )
    manager = forms.ModelChoiceField(
        queryset=Employee.objects.filter(position__department__title="Менеджер"),
        label="Менеджер",
        required=False,
    )
    engineer = forms.ModelChoiceField(
        queryset=Employee.objects.filter(position__department__title="(ПТО)"),
        label="Інженер ВТВ",
        required=False,
    )
    foreman = forms.ModelChoiceField(
        queryset=Employee.objects.filter(position__department__title="Прораб"),
        label="Прораб",
        required=False,
    )
    estimator = forms.ModelChoiceField(
        queryset=Employee.objects.filter(position__department__title="Кошторисний"),
        label="Кошторисник",
        required=False,
    )
    supply = forms.ModelChoiceField(
        queryset=Employee.objects.filter(position__department__title="Постачання"),
        label="Фахівець з постачання",
        required=False,
    )
    accountant = forms.ModelChoiceField(
        queryset=Employee.objects.filter(position__department__title="Бухгалтер"),
        label="Бухгалтер",
        required=False,
    )
    economist = forms.ModelChoiceField(
        queryset=Employee.objects.filter(position__department__title="Економіст"),
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
