from .models import Subject
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class SubjectIndex(LoginRequiredMixin, generic.ListView):
    # This view is only accessible to logged in users
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Subject
    template_name = 'timetable/subject_index.html'
    context_object_name = 'subject_list'

    def get_queryset(self):
        return Subject.objects.all()
