from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """
    Returns a range from 1 to the given value.
    """
    return range(1, value + 1)
