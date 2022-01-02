from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def split_timesince(value, delimiter=None):
    """カンマ区切りで2要素からなるtimesinceを分割してシンプルにする"""
    return value.split(delimiter)[0]