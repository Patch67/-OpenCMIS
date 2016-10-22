from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url
from . import views

app_name = "articles"


urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.Detail.as_view(), name='detail'),
    url(r'^add/$', views.Create.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.Update.as_view(), name='update'),
]
