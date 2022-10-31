from django import template

register = template.Library()

@register.filter
def unlist(value):
    return value.replace('[', '').replace(']', '').replace('\'','')