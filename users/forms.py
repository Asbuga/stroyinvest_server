from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.transaction import commit

from .models import Department, Employee, Position


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="", widget=forms.TextInput(attrs={"placeholder": "логін"})
    )
    password = forms.CharField(
        label="", widget=forms.PasswordInput(attrs={"placeholder": "пароль"})
    )


class UserEmployeeForm(UserCreationForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    position = forms.ModelChoiceField(queryset=Position.objects.all())
    birth_day = forms.DateField()
    mobile_phone = forms.CharField()
    internal_phone = forms.CharField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

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
