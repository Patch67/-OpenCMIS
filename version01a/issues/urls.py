from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url
from . import views

app_name = "issue"


urlpatterns = [
    # /issue/
    url(r'^$', views.Home.as_view(), name='home'),
    # /issue/add
    url(r'^add$', views.Create.as_view(), name='create'),
    # /issue/123
    url(r'^(?P<pk>[0-9]+)$', views.Detail.as_view(), name='detail'),
    # /issue/123/update
    url(r'^(?P<pk>[0-9]+)/update$', views.Update.as_view(), name='update'),
    # /issue/123/delete
    url(r'^(?P<pk>[0-9]+)/delete$', views.Delete.as_view(), name='delete'),
]
