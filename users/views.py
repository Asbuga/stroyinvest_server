from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from stroyinvest.models import BaseFormView

from .forms import CustomAuthenticationForm, UserEmployeeForm


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy("estimation:get_acts")


class CustomRegisterView(BaseFormView):
    form_class = UserEmployeeForm
    template_name = "stroyinvest/edit_form.html"
    success_url = reverse_lazy("estimation:get_acts")
    title_add = "Реєстрація користувача"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
