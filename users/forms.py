from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.transaction import commit

from .models import Department, Employee, Position


class DepartmentForm(forms.ModelForm):
    
    class Meta:
        model = Department
        fields = "__all__"
        


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "логін"})
    )
    password = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "пароль"})
    )


class UserEmployeeForm(UserCreationForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        label=Department._meta.get_field("title").verbose_name,
    )
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        label=Position._meta.get_field("title").verbose_name,
    )
    birth_day = forms.DateField(
        label=Employee._meta.get_field("birth_day").verbose_name
    )
    mobile_phone = forms.CharField(
        label=Employee._meta.get_field("mobile_phone").verbose_name
    )
    internal_phone = forms.CharField(
        label=Employee._meta.get_field("internal_phone").verbose_name
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        help_texts = {"username": "", "password": ""}
        labels = {"username": "Логін для входу"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def seve(self):
        user = super().save(commit=False)
        if commit:
            user.save()
            Employee.objects.create(
                user=user,
                department=self.changed_data["department"],
                position=self.changed_data["position"],
                birth_day=self.changed_data["department"],
                mobile_phone=self.changed_data["mobile_phone"],
                internal_phone=self.changed_data["internal_phone"],
            )
        return user
