# encoding=utf8
from django import template
from blog.models import Slider

register = template.Library()

@register.simple_tag()
def getSlides():
    return Slider.objects.filter(Publish__exact=True)
