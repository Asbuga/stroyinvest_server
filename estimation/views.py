from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View

from .filters import ContractFilter
from .forms import ActForm, AddendumForm, ContractForm
from .models import Act, Addendum, Contract
from .utils import FilterContent

EDIT_FORM = "stroyinvest/edit_form.html"


def get_acts(request):
    selected_acts = list(map(int, request.GET.getlist("selected_acts")))
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
    return render(request, "estimation/acts.html", context)


@login_required
def get_contracts(request):
    if request.GET.getlist("selected_contract"):
        selected_contract = list(map(int, request.GET.getlist("selected_contract")))
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


class ActFormView(LoginRequiredMixin, View):
    model = Act
    form_class = ActForm
    template_name = EDIT_FORM
    success_url = reverse_lazy("estimation:get_acts")

    def get_object(self):
        act_id = self.kwargs.get("act_id", None)
        return get_object_or_404(Act, id=act_id) if act_id else None

    def get(self, request, *args, **kwargs):
        act = self.get_object()

        if act is None:
            title = "Додати акт"
            button_delete = False
        else:
            title = "Редагувати акт"
            button_delete = True

        form = self.form_class(instance=act)
        context = {
            "form": form,
            "act": act,
            "title": title,
            "button_delete": button_delete,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        act = self.get_object()
        action = request.POST.get("action")
        form = self.form_class(data=request.POST, instance=act)

        if action == "post":
            if form.is_valid():
                form.save()
                return redirect(self.success_url)

        if action == "delete":
            act.delete()
            return redirect(self.success_url)

        context = {
            "form": form,
            "act": act,
        }
        return render(request, self.template_name, context)


class AddendumFormView(LoginRequiredMixin, View):
    model = Addendum
    form_class = AddendumForm
    template_name = EDIT_FORM
    success_url = reverse_lazy("estimation:get_contracts")

    def get_object(self):
        addendum_id = self.kwargs.get("addendum_id", None)
        return get_object_or_404(Addendum, id=addendum_id) if addendum_id else None

    def get(self, request, *args, **kwargs):
        addendum = self.get_object()

        if addendum is None:
            title = "Додати додаткову угоду"
            button_delete = False
        else:
            title = "Редагувати додаткову угоду"
            button_delete = True

        form = self.form_class(instance=addendum)
        context = {
            "form": form,
            "addendum": addendum,
            "title": title,
            "button_delete": button_delete,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        contract = self.get_object()
        action = request.POST.get("action")
        form = self.form_class(data=request.POST, instance=contract)

        if action == "post":
            if form.is_valid():
                form.save()
                return redirect(self.success_url)

        if contract == "delete":
            contract.delete()
            return redirect(self.success_url)

        context = {
            "form": form,
            "contract": contract,
        }
        return render(request, self.template_name, context)


class ContractFormView(LoginRequiredMixin, View):
    model = Contract
    form_class = ContractForm
    template_name = EDIT_FORM
    success_url = reverse_lazy("estimation:get_contracts")

    def get_object(self):
        contract_id = self.kwargs.get("contract_id", None)
        return get_object_or_404(Contract, id=contract_id) if contract_id else None

    def get(self, request, *args, **kwargs):
        contract = self.get_object()

        if contract is None:
            title = "Додати контракт"
            button_delete = False
        else:
            title = "Редагувати контракт"
            button_delete = True

        form = self.form_class(instance=contract)
        context = {
            "form": form,
            "contract": contract,
            "title": title,
            "button_delete": button_delete,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        contract = self.get_object()
        action = request.POST.get("action")
        form = self.form_class(data=request.POST, instance=contract)

        if action == "post":
            if form.is_valid():
                form.save()
                return redirect(self.success_url)

        if contract == "delete":
            contract.delete()
            return redirect(self.success_url)

        context = {
            "form": form,
            "contract": contract,
        }
        return render(request, self.template_name, context)
