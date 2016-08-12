from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Student


class IndexView(generic.ListView):
    template_name = 'opencmis/index.html'
    context_object_name = 'all_students'

    def get_queryset(self):
        return Student.objects.all()


class DetailView(generic.DetailView):
    model = Student
    template_name = 'opencmis/detail.html'


class UpdateView(generic.UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'ULN']
    template_name = 'opencmis/update.html'


class StudentCreate(CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'ULN']


class StudentUpdate(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'ULN']


class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('opencmis:index')
