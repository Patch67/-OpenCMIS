from django.conf.urls import url, include


from . import views

app_name = "opencmis"

'''New class based system'''
urlpatterns = [
    # url(regular_expression, view, name='view_name')
    # NB. view_name is so we can refer to this URL as opencmis:view_name
    # NB. if view is a class must use views.Class.as_view() to convert it into a view

    # /opencmis/student/
    url(r'student/$', views.IndexView.as_view(), name='index'),

    # /student/123/update/
    url(r'student/(?P<pk>[0-9]+)/update/$', views.StudentUpdate.as_view(), name='student-update'),

    # /student/add
    url(r'student/add/$', views.StudentCreate.as_view(), name='student-create'),

    # /student/123/delete/
    url(r'student/(?P<pk>[0-9]+)/delete/$', views.StudentDelete.as_view(), name='student-delete'),

    # /student/123/qualifications
    url(r'student/(?P<pk>[0-9]+)/qualification/$', views.StudentQualificationList.as_view(),
        name='student-qualification'),

    # /student/123/behaviours
    url(r'student/(?P<student_id>[0-9]+)/behaviour/$', views.behaviour_index,
        name='behaviour-index'),

    # /student/232/
    url(r'student/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),

]
