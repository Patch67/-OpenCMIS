from django.core.urlresolvers import reverse_lazy
from django.conf.urls import url
from . import views

app_name = "issue"


urlpatterns = [
    # /opencmis/issue/
    url(r'student/$',
        views.IndexView.as_view(), name='index'),
    ]