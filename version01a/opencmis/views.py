from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Student, StudentQualification


class IndexView(generic.ListView):
    template_name = 'opencmis/index.html'
    context_object_name = 'all_students'

    def get_queryset(self):
        return Student.objects.all()


class DetailView(generic.DetailView):
    model = Student
    template_name = 'opencmis/detail.html'


class StudentCreate(CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'ULN',
              'house', 'road', 'area', 'town', 'post_code']


class StudentUpdate(UpdateView):
    model = Student
    fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'ULN',
              'house','road', 'area', 'town', 'post_code']


class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('opencmis:index')


class StudentQualificationList(generic.ListView):
    model = StudentQualification
    template_name = 'opencmis/qualification_index.html'
    context_object_name = 'student_qualifications'

    def get_queryset(self):
        # TODO: How to pass Student.id or pk into next line
        return StudentQualification.objects.filter(student=1)