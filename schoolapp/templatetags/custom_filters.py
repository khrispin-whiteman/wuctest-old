from django import template

register = template.Library()

@register.simple_tag
def add(value, arg):
    return value + arg
