from django import template
from django.utils.timezone import now

register = template.Library()

@register.filter
def is_online(last_activity):
    if last_activity:
        return (now() - last_activity).total_seconds() < 20
    return False
