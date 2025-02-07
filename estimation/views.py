from datetime import datetime

from django.shortcuts import render

from .models import Contract


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
        'summ': summ,
        "months": months,
        "selected_month": selected_month,
        "years": years,
        "selected_year": selected_year,
    }
    return render(request, "estimation/table.html", context)
