from django.views.generic import ListView
from .models import Device


class Home(ListView):
    model = Device
    template_name = 'monitor/home.html'
    queryset = Device.objects.all()


