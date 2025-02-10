from datetime import datetime

from django.shortcuts import render, redirect
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from .models import Contract, Act
from .forms import ActCreateNew, ContractCreateNew


@login_required
def table(request):
    # Для вибору місяця (періоду закриття актів).
    months = [
        ("Січень", "Січень"),
        ("Лютий", "Лютий"),
        ("Березень", "Березень"),
        ("Квітень", "Квітень"),
        ("Травень", "Травень"),
        ("Червень", "Червень"),
        ("Липень", "Липень"),
        ("Серпень", "Серпень"),
        ("Вересень", "Вересень"),
        ("Жовтень", "Жовтень"),
        ("Листопад", "Листопад"),
        ("Грудень", "Грудень"),
    ]
    selected_month = request.GET.get("month", "13")

    # Для вибору року закриття актів.
    current_year = datetime.now().year
    years = [str(year) for year in range(current_year, current_year - 5, -1)]
    selected_year = request.GET.get("year", current_year)
    selected_year = int(selected_year) if selected_year else current_year

    # Для вибраних актів.
    selected_acts = list(map(int, request.GET.getlist("selected_acts")))

    # Для вибору актів та контрактів.
    contracts = Contract.objects.prefetch_related("acts").all()

    summ = 0
    filtering_contracts = []
    for contract in contracts:
        acts = contract.acts.filter(year=selected_year)

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
        "months": months,
        "selected_month": selected_month,
        "years": years,
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
    pass


@login_required
def add_contract(request):
    if request.method == "POST":
        form = ContractCreateNew(request.POST)
        if form.is_valid():
            form.save()
            return redirect("estimation/table.html")
    else:
        form = ContractCreateNew()
    return render(
        request, "estimation/contract/add_contract.html", context={"form": form}
    )


@login_required
def edit_contract(request, contract_id):
    contract = Contract.objects.get(id=contract_id)
    if request.method == "POST":
        form = ContractCreateNew(instance=contract, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("estimation:table")
    else:
        form = ContractCreateNew(instance=contract)
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
        acts_summ = Act.objects.filter(contract=contract).aggregate(Sum("summ"))['summ__sum']
        print(acts_summ)
        contract_performance.append(
            {
                "contract": contract,
                "acts_summ": acts_summ,
                "balance": contract.summ - acts_summ
            }
        )

    return render(
        request,
        "estimation/contract/contracts.html",
        context={"contract_performance": contract_performance},
    )
