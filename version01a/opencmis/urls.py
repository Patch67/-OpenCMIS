from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url
from . import views

app_name = "opencmis"

'''New class based system'''
urlpatterns = [
    # url(regular_expression, view, name='view_name')
    # NB. view_name is so we can refer to this URL as opencmis:view_name
    # NB. if view is a class must use views.Class.as_view() to convert it into a view

    # /opencmis/student/
    url(r'student/$',
        views.IndexView.as_view(),
        name='index'),

    # /opencmis/student/232/
    url(r'student/(?P<pk>[0-9]+)/$',
        views.DetailView.as_view(),
        name='student-detail'),

    # /opencmis/student/gmail
    url(r'student/gmail/$',
        views.gmail,
        name='gmail'),

    # /student/123/update/
    url(r'student/(?P<pk>[0-9]+)/update/$',
        views.StudentUpdate.as_view(),
        name='student-update'),

    # /student/add
    url(r'student/add/$',
        views.StudentCreate.as_view(),
        name='student-create'),

    # /student/123/delete/
    url(r'student/(?P<pk>[0-9]+)/delete/$',
        views.StudentDelete.as_view(),
        name='student-delete'),

    # STUDENT QUALIFICATIONS
    # LIST
    # /student/123/qualifications
    url(r'student/(?P<student_id>[0-9]+)/qualification/$',
        views.StudentQualificationList.as_view(),
        name='student-qualification'),

    # /student/123/qualifications/add
    url(r'student/(?P<student_id>[0-9]+)/qualification/add/$',
        views.StudentQualificationAdd.as_view(),
        name='student-qualification-create'),

    # UPDATE
    # /student/123/qualifications/123/update
    url(r'student/(?P<student_id>[0-9]+)/qualification/(?P<qualification_id>[0-9]+)/update$',
        views.StudentQualificationUpdate.as_view(
            success_url=reverse_lazy('opencmis:student-qualification')),
        name='student-qualification-update'),

    # /student/123/behaviours
    url(r'student/(?P<student_id>[0-9]+)/behaviour/$',
        views.behaviour_index,
        name='behaviour-index'),

    # /student/123/baseline
    url(r'student/(?P<student_id>[0-9]+)/baseline/$',
        views.BaselineIndex.as_view(),
        name='baseline'),

    # /student/123/baseline/3/add
    url(r'student/(?P<student_id>[0-9]+)/baseline/(?P<heading>[0-9]+)/add/$',
        views.BaselineAdd.as_view(),
        name='baseline-add'),

    # /ilr/
    url(r'ilr/$', views.ILR, name='ilr'),

    # /dashboard/
    url(r'dashboard/$', views.dashboard, name='dashboard'),
]
