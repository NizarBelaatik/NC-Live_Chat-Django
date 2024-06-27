from django import template
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def next_elem_in_for(sequence, position):
    try:
        return sequence[int(position)+1]
    except IndexError:
        return None
    

@register.filter
def custom_timesince(value):
    if not isinstance(value, datetime):
        return value

    # Convert naive datetime to aware datetime
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())

    now = timezone.now()
    time_diff = timesince(value, now)

    # Replace 'hours' with 'h' and 'minutes' with 'min'
    time_diff = time_diff.replace('hour', 'h')
    time_diff = time_diff.replace('minutes', 'min').replace('minute', 'min')
    time_diff = time_diff.replace('days', 'd').replace('day', 'd')

    return time_diff



@register.filter
def custom_timesince_2(value):
    # Replace 'hours' with 'h' and 'minutes' with 'min'
    value = value.replace('hours', 'h').replace('hour', 'h')
    value = value.replace('minutes', 'min').replace('minute', 'min')
    value = value.replace('days', 'd').replace('day', 'd')
    return value