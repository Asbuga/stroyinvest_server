from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy

from stroyinvest.models import BaseFormView

from .filters import ContractFilter, ActFilter
from .forms import ActForm, AddendumForm, ContractForm
from .models import Act, Addendum, Contract


EDIT_FORM = "stroyinvest/edit_form.html"


class ActFormView(BaseFormView):
    model = Act
    form_class = ActForm
    template_name = EDIT_FORM
    success_url = reverse_lazy("estimation:get_acts")
    title_add = "Додати акт"
    title_edit = "Редагувати акт"


class AddendumFormView(BaseFormView):
    model = Addendum
    form_class = AddendumForm
    template_name = EDIT_FORM
    success_url = reverse_lazy("estimation:get_contracts")
    title_add = "Додати додаткову угоду"
    title_edit = "Редагувати додаткову угоду"


class ContractFormView(BaseFormView):
    model = Contract
    form_class = ContractForm
    template_name = EDIT_FORM
    success_url = reverse_lazy("estimation:get_contracts")
    title_add = "Додати контракт"
    title_edit = "Редагувати контракт"


def get_acts(request):
    if request.GET.getlist("selected"):
        selected = list(map(int, request.GET.getlist("selected")))
        acts = Act.objects.filter(id__in=selected)
        contracts = Contract.objects.filter(
            id__in=acts.values("contract_id")
        ).order_by("type", "number", "-date_signing")
    else:
        contracts = Contract.objects.order_by("type", "number", "-date_signing").all()
        acts = Act.objects.all()

    act_filter = ActFilter(request.GET, queryset=acts)
    acts = act_filter.qs

    summ = 0
    filtering_contracts = []
    for contract in contracts:
        try:
            acts = Act.objects.filter(contract=contract).filter(id__in=selected).all()
        except NameError:
            acts = Act.objects.filter(contract=contract).all()        

        if acts.exists():
            filtering_contracts.append({"contract": contract, "acts": acts})

        if contract.type == "ГП":
            for act in acts:
                summ += act.summ

    context = {
        "title": "Виконання",
        "filter": act_filter,
        "filtering_contracts": filtering_contracts,
        "summ": summ,
    }
    return render(request, "estimation/acts.html", context)


@login_required
def get_contracts(request):
    if request.GET.getlist("selected"):
        selected_contract = list(map(int, request.GET.getlist("selected")))
        contracts = Contract.objects.filter(id__in=selected_contract).order_by(
            "-date_signing"
        )
    else:
        contracts = Contract.objects.order_by("-date_signing").all()
    contract_filter = ContractFilter(request.GET, queryset=contracts)

    contracts_summ = 0
    balance_all = 0
    performance_contract = []

    for contract in contract_filter.qs:
        addendums = Addendum.objects.filter(contract=contract).order_by("number").all()
        acts_summ = Act.objects.filter(contract=contract).aggregate(Sum("summ"))
        acts_summ = acts_summ["summ__sum"] if acts_summ["summ__sum"] is not None else 0

        contracts_summ += contract.summ

        balance = contract.summ - acts_summ
        balance_all += balance

        performance_contract.append(
            {
                "contract": contract,
                "addendums": addendums,
                "acts_summ": acts_summ,
                "balance": balance,
            }
        )

    return render(
        request,
        "estimation/contracts.html",
        context={
            "title": "Контракти",
            "filter": contract_filter,
            "performance_contract": performance_contract,
            "contracts_summ": contracts_summ,
            "balance_all": balance_all,
            "contracts_balance": contracts_summ - balance_all,
        },
    )
