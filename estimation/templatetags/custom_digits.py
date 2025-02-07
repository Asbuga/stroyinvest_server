from django import template
from django.template.defaultfilters import stringfilter
import locale


register = template.Library()

@register.filter(name='format_number')
@stringfilter
def format_number(value):
    try:
        locale.setlocale(locale.LC_NUMERIC, "uk_UA.UTF-8")
    except locale.Error:
        locale.setlocale(locale.LC_NUMERIC, "")
    
    return locale.format_string("%.2f", float(value), grouping=True).replace(",", " ").replace(".", ",")
