from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url
from . import views

app_name = "timetable"

'''New class based system'''
urlpatterns = [
    # url(regular_expression, view, name='view_name')
    # NB. view_name is so we can refer to this URL as appname:view_name
    # NB. if view is a class must use views.Class.as_view() to convert it into a view

    # /opencmis/student/
    url(r'subject/$', views.SubjectIndex.as_view(), name='index'),
    ]
