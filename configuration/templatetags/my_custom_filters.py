from django import template

register = template.Library()

@register.filter(name='get_penultimate')
def get_penultimate(value):
    """Retourne l'avant-dernier élément de la liste."""
    try:
        return value[-2]
    except IndexError:
        return None
    
