from lib2to3.fixes.fix_input import context

from django.shortcuts import render

from .models import Contract


def table(request):
    contracts = Contract.objects.get_subject_contract_name()
    context = {'contracts': contracts}
    return render(request, 'estimation/table.html', context)
