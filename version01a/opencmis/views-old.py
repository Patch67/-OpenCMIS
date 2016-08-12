from django.shortcuts import render
from django.http import HttpResponse


def dashboard(request):
    html = '<div>Dashboard</div>'
    return HttpResponse(html)


def student_index(request):
    html = '<div>Student Index</div>'
    return HttpResponse(html)


def teacher_index(request):
    html = '<div>Teacher Index</div>'
    return HttpResponse(html)


def qualification_index(request):
    html = '<div>Qualification Index</div>'
    return HttpResponse(html)


def building_index(request):
    html = '<div>Building Index</div>'
    return HttpResponse(html)