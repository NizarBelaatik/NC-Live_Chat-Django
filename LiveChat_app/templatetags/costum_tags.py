from django import template

register = template.Library()

@register.filter
def next_elem_in_for(sequence, position):
    try:
        return sequence[int(position)+1]
    except IndexError:
        return None