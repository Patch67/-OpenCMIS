from django.conf.urls import url, include
from . import views

app_name = "opencmis"

'''New class based system'''
urlpatterns = [
    # /opencmis/student/
    url(r'student/$', views.IndexView.as_view(), name='index'),

    # /student/232/
    url(r'^student/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

    # /student/123/update/
    url(r'student/(?P<pk>[0-9]+)/update/$', views.StudentUpdate.as_view(), name='student-update'),

    # /student/add
    url(r'student/add/$', views.StudentCreate.as_view(), name='student-create'),

    # /student/123/delete/
    url(r'student/(?P<pk>[0-9]+)/delete/$', views.StudentDelete.as_view(), name='student-delete'),

]

