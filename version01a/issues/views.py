from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Issue, Update as My_Update


class Home(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Issue
    template_name = 'issue/home.html'
    queryset = Issue.objects.all()

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['index'] = index_context(self.request)
        return context


class Detail(LoginRequiredMixin, DetailView):
    # TODO: Can't make this type of View into a one/many form/subform
    # http://stackoverflow.com/questions/8903601/how-to-process-a-form-via-get-or-post-using-class-based-views

    # TODO: Readme for Ajax and Forms
    # https://docs.djangoproject.com/en/1.10/topics/class-based-views/generic-editing/

    login_url = reverse_lazy('login')
    model = Issue
    template_name = 'issue/detail.html'

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        context['updates'] = My_Update.objects.filter(issue=self.kwargs['pk'])
        context['index'] = index_context(self.request)
        return context


class Create(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    permission_required = 'issue.create_issue'
    model = Issue
    template_name = 'issue/issue-form.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        context['index'] = index_context(self.request)
        return context


class Update(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    permission_required = 'issue.change_issue'
    model = Issue
    template_name = 'issue/issue-form.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        context['index'] = index_context(self.request)
        return context


class Delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    permission_required = 'issue.delete_issue'
    model = Issue
    success_url = reverse_lazy('issue:home')

    def get_context_data(self, **kwargs):
        context = super(Delete, self).get_context_data(**kwargs)
        context['index'] = index_context(self.request)
        return context


def index_context(request):
    """index filtering and search"""
    # Check to see if index is limited via filter
    f = request.GET.get('filter')
    if f and f != "Any":
        index = Issue.objects.filter(status=f)
    else:
        index = Issue.objects.all()
    # Check to see if index is limited via search
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        if len(query_list) == 1:
            print("Query_list = {0}".format(query_list))
            index = index.filter(Q(title__contains=query_list[0]) or Q(summary__contains=query_list[0]))
    paginator = Paginator(index, 20)  # Limit to 20 entries per page, then paginate
    page = request.GET.get('page')
    try:
        index = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        index = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        index = paginator.page(paginator.num_pages)
    # Now we've finished refining index simply pass it to the context dictionary
    return index


