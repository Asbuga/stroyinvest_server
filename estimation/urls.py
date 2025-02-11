"""
URL configuration for stroyinvest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from . import views


app_name = "estimation"
urlpatterns = [
    path("table/", views.table, name="table"),

    # Act.
    path("act/add/", views.add_act, name="add_act"),
    path("act/edit/<int:act_id>", views.edit_act, name="edit_act"),

    # Contract.
    path("contracts/", views.get_contracts, name="get_contracts"),
    path("contract/add/", views.ContractFormView.as_view(), name="add_contract"),
    path("contract/edit/<int:contract_id>", views.ContractFormView.as_view(), name="edit_contract"),
    path("contract/delete/<int:contract_id>", views.delete_contract, name="delete_contract"),

    # Addendum.
    path("addendums/", views.get_addendums, name="get_addendums"),
    path("addendum/add/", views.add_addendum, name="add_addendum"),
    path("addendum/edit/<int:addendum_id>", views.edit_addendum, name="edit_addendum"),
    path("addendum/delete/<int:addendum_id>", views.delete_addendum, name="delete_addendum"),
]
