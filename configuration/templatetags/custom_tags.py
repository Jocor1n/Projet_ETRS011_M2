from django import template

register = template.Library()

@register.simple_tag
def update_variable(value):
    """Permet de mettre à jour une variable existante dans le template"""
    return value

