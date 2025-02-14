from django.urls import path

from . import views


app_name = "estimation"
urlpatterns = [
    # Act.
    path("acts/", views.get_acts, name="get_acts"),
    path("act/add/", views.ActFormView.as_view(), name="add_act"),
    path("act/edit/<int:id>", views.ActFormView.as_view(), name="edit_act"),

    # Addendum.
    path("addendum/add/", views.AddendumFormView.as_view(), name="add_addendum"),
    path("addendum/edit/<int:id>", views.AddendumFormView.as_view(), name="edit_addendum"),
    
    # Contract.
    path("contracts/", views.get_contracts, name="get_contracts"),
    path("contract/add/", views.ContractFormView.as_view(), name="add_contract"),
    path("contract/edit/<int:id>", views.ContractFormView.as_view(), name="edit_contract"),
]
