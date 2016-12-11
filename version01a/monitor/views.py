from django.http import HttpResponse
from django.shortcuts import render
from .models import Device


def home(request):
    """
    This is an exploration of function based views.
    In particular it is an exploration low level GET and POST methods
    :param request:
    :return:
    """
    context = {}
    context['title'] = "Home"
    if request.method == 'GET':
        context['method'] = "GET"
    elif request.method == 'POST':
        context['method'] = "POST"
    return render(request, 'monitor/home.html', context)




