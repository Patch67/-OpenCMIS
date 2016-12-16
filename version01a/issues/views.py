from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
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


# class Detail(LoginRequiredMixin, DetailView):
class Detail(LoginRequiredMixin, UpdateView):
    # PAB 02/12/2016 Renamed this to old so I can start a new class called Detail
    # based on the FormView
    # PAB 02/12/2016
    # I originally used just a DetailView which works fine for output only forms
    # but this form is a bit different because I also want to do some input, i.e. I want to POST update data to it.
    # I changed from a DetailView to an UpdateView and tried to work with the Post functions but it still doesn't work.
    # I wonder whether I should just bite the bullet and make my own FormView.
    # This appears to allow me to do anything with forms whereas the predefined Views are specifically limited to
    # certain situations.

    login_url = reverse_lazy('login')
    model = Issue
    template_name = 'issue/detail.html'
    fields = '__all__'  # Needed to add this in if changing from DetailView to UpdateView

    def get_context_data(self, **kwargs):
        context = super(Detail, self).get_context_data(**kwargs)
        context['updates'] = My_Update.objects.filter(issue=self.kwargs['pk'])
        context['index'] = index_context(self.request)
        return context

    def form_valid(self, form):
        # TODO: This never seems to get called
        print("Hello world")
        print(form)
        return super(Detail, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        This is only called when a user Clicks the Update button and the update form is submitted.
        If the page is called via a GET command this is not called.
        :param request: Use request.POST to get the form data from the Update section
        :param args:
        :param kwargs: Use kwargs['pk'] to get the issue id from the URL
        :return:
        """
        # TODO: Do we need two forms here; one for issue record and one for update record?
        if request.method == 'POST':
            # Work out which form was posted, note that accessing a non existent form element raises an exception
            form = "None"  # Just a starting value
            try:
                print(request.POST['Status'])
                if request.POST['Status']:
                    form = "Issue"
            except MultiValueDictKeyError:
                pass

            try:
                print(request.POST['Public'])
                if request.POST['Public']:
                    form = "Comment"
            except MultiValueDictKeyError:
                pass

            if form == "Issue":
                q = Issue.objects.get(pk=kwargs['pk'])
                print(request.POST['Status'])
                if request.POST['Status'] == "Open":
                    q.status = "O"
                elif request.POST['Status'] == "Close":
                    q.status = "C"
                elif request.POST['Status'] == "On hold":
                    q.status = "H"
                print("make is so {0}".format(q.status))
                q.save()
            elif form == "Comment":
                q = My_Update(issue=Issue.objects.get(pk=kwargs['pk']),
                              date=timezone.now(),
                              personnel=User.objects.get(username=request.user.username),
                              update=request.POST['Update'])  # TODO: This doesn't do any validation
                q.save()

        return HttpResponseRedirect('/issue/{0}'.format(kwargs['pk']))


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


