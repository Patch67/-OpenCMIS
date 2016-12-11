from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
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
        # Any test of POST['data'] will cause an exception if not present
        # So use a try catch to avoid the exception
        # At the end either has_data will be true if it existed else false

        has_data = False
        try:
            print(request.POST['data'])
            has_data = True
        except MultiValueDictKeyError:
            pass
        if has_data:
            context['data'] = request.POST['data']

    return render(request, 'monitor/home.html', context)




