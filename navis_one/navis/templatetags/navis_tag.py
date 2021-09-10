from django import template
from ..models import Category, Filter


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_filter():
    return Filter.objects.all()
