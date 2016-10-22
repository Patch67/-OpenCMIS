
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Article
    template_name = 'articles/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        return Article.objects.all()


class Detail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Article
    template_name = 'articles/detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        context['article_list'] = Article.objects.all()
        return context


class Create(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'author', 'tags', 'body']
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_object(self):
        return get_object_or_404(Article, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        context['article_list'] = Article.objects.all()
        return context


class Update(LoginRequiredMixin, UpdateView):
    model = Article
    fields = ['title', 'author', 'tags', 'body']
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get_object(self):
        return get_object_or_404(Article, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        context['article_list'] = Article.objects.all()
        return context
