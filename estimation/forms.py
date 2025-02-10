from django import forms

from .models import Act, Contract


class ContractCreateNew(forms.ModelForm):
    class Meta:
        model = Contract
        fields = "__all__"
        widgets = {
            "subject_contract": forms.Textarea(attrs={"rows": 6}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"



class ActCreateNew(forms.ModelForm):
    class Meta:
        model = Act
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"
