from django import template

register = template.Library()

@register.filter(name='lookup_author')
def lookup_author(val, arg):
    return val[arg]['Author']

@register.filter(name='lookup_ingredients')
def lookup_ingredients(val, arg):
    return val[arg]['Ingredients']

@register.filter(name='lookup_directions')
def lookup_directions(val, arg):
    return val[arg]['Directions']