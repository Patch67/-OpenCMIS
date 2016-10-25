# See template library tutorial here ...
# http://vanderwijk.info/blog/adding-css-classes-formfields-in-django-templates/
from django.template import Library

register = Library()


@register.filter(name='add_css')
def add_css(field, css):
    return field.as_widget(attrs={"class": css})
