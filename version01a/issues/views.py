from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Issue


# Create your views here.
class Home(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Issue
    template_name = 'issue/home.html'
    context_object_name = "index"
    queryset = Issue.objects.all()

