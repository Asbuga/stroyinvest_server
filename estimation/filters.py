import django_filters
from django.db.models import Min, Max
from .models import Act, Contract


class ActFilter(django_filters.FilterSet):
    class Meta:
        model = Act
        fields = ["period", "year"]


def get_сontract_year_choices():
    years = Contract.objects.aggregate(
        min_year=Min("date_signing"), max_year=Max("date_signing")
    )
    if not years["min_year"] or not years["max_year"]:
        return []
    return [
        (str(year), str(year))
        for year in range(years["min_year"].year, years["max_year"].year + 1)
    ]


class ContractFilter(django_filters.FilterSet):
    year = django_filters.ChoiceFilter(
        field_name="date_signing", lookup_expr="year", empty_label=None
    )
    
    class Meta:
        model = Contract
        fields = ["year", "customer", "type", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["year"].extra["choices"] = [("", "Всі роки")] + get_сontract_year_choices()
