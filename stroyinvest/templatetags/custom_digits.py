import locale

from django import template


register = template.Library()


@register.filter
def format_currency(value):
    """
    Formats a number as "100,000,000.00" according to the Django locale.
    """
    try:
        value = float(value)
        locale.setlocale(locale.LC_NUMERIC, "uk_UA.UTF-8")
        return locale.format_string("%.2f", value, grouping=True)
    except (ValueError, TypeError):
        return value
