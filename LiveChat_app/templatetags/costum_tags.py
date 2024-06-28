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
    time_diff = now - value

    sec =time_diff.total_seconds()
    minutes = float(time_diff.total_seconds() // 60)
    hours = float(minutes // 60)
    day = float(hours // 24)
    month=float(day // 30)
    year=float(month // 12)


    # Custom formatting based on the time difference
    if year>0:
        if year == 1:
            return f"{int(year)} year ago"
        else:
            return f"{int(year)} years ago"
    elif month>0:
        if month == 1:
            return f"{int(month)} month ago"
        else:
            return f"{int(month)} months ago"
    elif day>0:
        if day ==1:
            return f"{int(day)} day ago"
        else:
            return f"{int(day)} days ago"
    elif hours > 0 and hours < 24:
        if ((minutes+15)//60 > hours):
            return f"{int(hours+1)}h ago"
        else:
            return f"{int(hours)}h ago"
    
    elif minutes < 60:
        return f"{int(minutes)}min ago"
    elif minutes < 1:
        return "just now"
    else:
        return f"{time_diff} ago"


    
@register.filter
def custom_timesince_2(value): 
    # Replace 'hours' with 'h' and 'minutes' with 'min'
    # {{ data.data_TIME|timesince|custom_timesince_2  }}
    value = value.replace('hours', 'h').replace('hour', 'h')
    value = value.replace('minutes', 'min').replace('minute', 'min')
    value = value.replace('days', 'd').replace('day', 'd')
    return value

