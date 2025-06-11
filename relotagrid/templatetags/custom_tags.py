from django import template

register = template.Library()

@register.simple_tag
def get_note(grille, element_control, critere):
    return grille.notes.filter(element_controle=element_control, critere=critere).first()
