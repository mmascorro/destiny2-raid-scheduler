from django import template
from django.utils.html import format_html
import datetime

register = template.Library()


@register.inclusion_tag('board/tags/time_tag.html')
def time_tag(dt):
  return {
    'dt': dt
  }


@register.filter()
def nextDay(start):
   newDate = start + datetime.timedelta(days=1)
   return newDate

@register.filter()
def prevDay(start):
   newDate = start + datetime.timedelta(days=-1)
   return newDate