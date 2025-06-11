from django import template

register = template.Library()

@register.filter
def split(value, separator=","):
    return value.split(separator)

@register.filter
def index(sequence, position):
    try:
        return sequence[int(position) - 1]  # car mois = 1 à 12
    except:
        return ''
