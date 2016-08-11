from django.conf.urls import url, include
from . import views

urlpatterns = [
    # /opencmis/
    url(r'^$', views.dashboard, name='dashboard'),
    # /opencmis/student/
    url(r'^student/$', views.student_index, name='student_index'),
    # /opencmis/teacher/
    url(r'^teacher/$', views.teacher_index, name='teacher_index'),
    # /opencmis/qualification/
    url(r'^qualification/$', views.qualification_index, name='qualification_index'),
    # /opencmis/building/
    url(r'^building/$', views.building_index, name='building_index'),

]
