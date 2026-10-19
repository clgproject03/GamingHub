from django import template

register = template.Library()


@register.filter
def times(number):
    try:
        return range(int(number))
    except (TypeError, ValueError):
        return range(0)


@register.filter
def star_range(rating):
    try:
        return range(int(round(float(rating))))
    except (TypeError, ValueError):
        return range(0)


@register.filter
def empty_star_range(rating):
    try:
        return range(5 - int(round(float(rating))))
    except (TypeError, ValueError):
        return range(5)


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0
