from django import template
from ..models import item


register=template.Library()

@register.simple_tag

def total_item():
    return item.objects.count()