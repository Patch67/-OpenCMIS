from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url
from . import views

app_name = "monitor"

'''New class based system'''
urlpatterns = [
    # url(regular_expression, view, name='view_name')
    # view_name is so we can refer to this URL as opencmis:view_name
    # If view is a class must use views.Class.as_view() to convert it into a view
    # If view is a function use views.function

    # /monitor/
    url(r'monitor/$', views.home, name='home'),
]
