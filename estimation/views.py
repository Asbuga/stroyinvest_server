from datetime import datetime

from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import View


from .models import Contract, Act
from .forms import ActCreateNew, ContractCreateForm
from .utils import FilterContent


@login_required
def table(request):
    # Для вибраних актів.
    selected_acts = list(map(int, request.GET.getlist("selected_acts")))

    # Для вибору актів та контрактів.
    contracts = Contract.objects.prefetch_related("acts").all()

    select = FilterContent(request)

    selected_year = select.get_selected_year()
    selected_month = select.get_selected_month()

    summ = 0
    filtering_contracts = []
    for contract in contracts:
        if selected_year != "Всі":
            acts = contract.acts.filter(year=selected_year)
        else:
            acts = contract.acts.all()

        if selected_month != "13":
            acts = acts.filter(period=selected_month)

        if selected_acts:
            acts = acts.filter(id__in=selected_acts)

        if acts.exists():
            filtering_contracts.append({"contract": contract, "acts": acts})

        if contract.type == "ГП":
            for act in acts:
                summ += act.summ

    context = {
        "filtering_contracts": filtering_contracts,
        "summ": summ,
        "months": select.MONTH,
        "selected_month": selected_month,
        "years": select.years,
        "selected_year": selected_year,
    }
    return render(request, "estimation/table.html", context)


@login_required
def add_act(request):
    if request.method == "POST":
        form = ActCreateNew(request.POST)
        if form.is_valid():
            form.save()
            return redirect("estimation/table.html")
    else:
        form = ActCreateNew()
    return render(request, "estimation/act/add_act.html", context={"form": form})


@login_required
def edit_act(request, act_id):
    act = Act.objects.get(id=act_id)
    if request.method == "POST":
        form = ActCreateNew(instance=act, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("estimation:table")
    else:
        form = ActCreateNew(instance=act,)
    return render(request, "estimation/act/edit_act.html", context={"form": form, "act": act})


@login_required
def add_contract(request):
    if request.method == "POST":
        form = ContractCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("estimation:get_contracts")
    else:
        form = ContractCreateForm()
    return render(
        request, "estimation/contract/add_contract.html", context={"form": form}
    )



class ContractFormView(View):
    model = Contract
    form_class = ContractCreateForm
    template_name = "estimation/contract_form.html"
    success_url = reverse_lazy("estimation:get_contracts")
    

    def get_object(self):
        contract_id = self.kwargs.get("contract_id", None)
        return get_object_or_404(Contract, id=contract_id) if contract_id else None

    
    def get(self, request, *args, **kwargs):
        contract = self.get_object()
        form = self.form_class(instance=contract)
        context = {
            "form": form,
            "contract": contract,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        title = "Редагувати контракт"
        contract = self.get_object()
        action = request.POST.get("action")
        
        form = self.form_class(request.POST, instance=contract)

        if action == "post":
            if form.is_valid():
                form.save()
                return redirect(self.success_url)
        
        if contract:
            contract.delete()
            return redirect(self.success_url)
    
        context = {"form": form, "contract": contract, "title": title}
        return render(request, self.template_name, context)    



@login_required
def edit_contract(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    if request.method == "POST":
        form = ContractCreateForm(instance=contract, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("estimation:get_contracts")
    else:
        form = ContractCreateForm(instance=contract)
    return render(
        request,
        "estimation/contract/edit_contract.html",
        context={"form": form, "contract": contract},
    )


@login_required
def get_contracts(request):
    contract_performance = []
    contracts = (
        Contract.objects.filter(type="ГП").order_by("contractor", "date_signing").all()
    )
    for contract in contracts:
        acts_summ = Act.objects.filter(contract=contract).aggregate(Sum("summ"))[
            "summ__sum"
        ]
        
        if acts_summ is None:
            acts_summ = 0

        balance = contract.summ - acts_summ

        contract_performance.append(
            {
                "contract": contract,
                "acts_summ": acts_summ,
                "balance": balance,
            }
        )

    return render(
        request,
        "estimation/contract_overview.html",
        context={"contract_performance": contract_performance},
    )


def get_contract(request):
    return render(request, "estimation/contract/contract.html")


def delete_contract(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    if request.method == "DELETE":
        contract.delete()
        redirect("estimation:get_contracts")
    else:
        pass


# Addendum.
def get_addendums(request):
    title = "Додаткові угоди"
    pass
        
def add_addendum(request):
    title = "Додати додаткову угоди"
    pass
    
def edit_addendum(request, contract_id):
    title = "Редагувати додаткову угоди"
    pass
    
def delete_addendum(request, contract_id):
    title = "Видалити угоди"
    pass
