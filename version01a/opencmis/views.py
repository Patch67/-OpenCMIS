from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Student, StudentQualification, Behaviour, BaselineAssessment, Qualification, Header, BaselineValue, BaselineEntry
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class IndexView(LoginRequiredMixin, ListView):
    # This view is only accessible to logged in users
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Student
    template_name = 'opencmis/index.html'
    context_object_name = 'student_list'
    permission_required = 'opencmis.student_reader'

    def get_context_data(self, **kwargs):
        """Customise the context ready to supply to the template"""
        context = super(IndexView, self).get_context_data(**kwargs)
        # The following two lines should appear in every context
        context['student'] = 'No body'
        context['tab'] = ''
        return context

    def get_queryset(self):
        return Student.objects.all()


class DetailView(DetailView):
    model = Student
    template_name = 'opencmis/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['student_list'] = Student.objects.all()
        return context


class StudentCreate(CreateView):
    model = Student
    fields = ['status', 'title', 'first_name', 'last_name', 'date_of_birth',
              'gender', 'ethnicity', 'ULN',
              'house', 'road', 'area', 'town', 'post_code']

    def get_object(self):
        return get_object_or_404(Student, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StudentCreate, self).get_context_data(**kwargs)
        context['student_list'] = Student.objects.all()
        return context


class StudentUpdate(UpdateView):
    model = Student
    fields = ['status', 'title', 'first_name', 'last_name', 'date_of_birth',
              'ethnicity', 'gender', 'ULN',
              'house', 'road', 'area', 'town', 'post_code']

    def get_object(self):
        return get_object_or_404(Student, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StudentUpdate, self).get_context_data(**kwargs)
        context['student_list'] = Student.objects.all()
        return context


class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('opencmis:index')

    def get_context_data(self, **kwargs):
        context = super(StudentDelete, self).get_context_data(**kwargs)
        context['student_list'] = Student.objects.all()
        return context


class StudentQualificationList(ListView):
    model = StudentQualification
    template_name = 'opencmis/qualification_index.html'
    context_object_name = 'qual_list'

    def get_context_data(self, **kwargs):
        """Customise the context ready to supply to the template"""
        context = super(StudentQualificationList, self).get_context_data(**kwargs)
        context['student_list'] = Student.objects.all()
        # The following two lines should appear in every context
        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_id'])
        context['tab'] = 'qualification'
        return context

    def get_queryset(self):
        # Get the student id from the key word arguments and filter the related quals
        return StudentQualification.objects.filter(student=self.kwargs['student_id'])


class StudentQualificationAdd(CreateView):
    model = StudentQualification
    fields = ['student', 'qualification', 'start', 'expected_end']

    def get_object(self):
        return get_object_or_404(StudentQualification, pk=self.kwargs['studentqualification_id'])

    def get_context_data(self, **kwargs):
        context = super(StudentQualificationAdd, self).get_context_data(**kwargs)
        context['student_list'] = Student.objects.all()
        # The following two lines should appear in every context
        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_id'])
        context['tab'] = 'qualification'
        print(context)
        return context


class StudentQualificationUpdate(UpdateView):
    model = StudentQualification
    fields = ['student', 'qualification', 'start', 'expected_end']

    def get_object(self):
        return get_object_or_404(StudentQualification, pk=self.kwargs['qualification_id'])

    def get_context_data(self, **kwargs):
        context = super(StudentQualificationUpdate, self).get_context_data(**kwargs)
        context['student_list'] = Student.objects.all()
        # The following two lines should appear in every context
        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_id'])
        context['tab'] = 'qualification'
        return context


def student_qualification_index(request, student_id):
    template = 'opencmis/qualification_index.html'
    context = {'student': get_object_or_404(Student, pk=student_id)} # Define context as a dictionary
    context['qualification_list'] = StudentQualification.objects.filter(student=student_id)
    context['student_list'] = Student.objects.all()     # Add entry to dictionary
    context['tab'] = 'qualification'
    return render(request, template, context)


def behaviour_index(request, student_id):
    template = 'opencmis/behaviour_index.html'
    context = {'student': get_object_or_404(Student, pk=student_id)}
    context['behaviour_list'] = Behaviour.objects.filter(student=student_id)
    context['student_list'] = Student.objects.all()     # Add entry to dictionary
    context['tab'] = 'behaviour'
    return render(request, template, context)


def baseline_detail(request, student_id):
    template = 'opencmis/baseline.html'
    context = {'student': get_object_or_404(Student, pk=student_id)}
    # get_or_create on the next line to create the BaselineAssessment if it doesn't already exist
    context['baseline_detail'] = BaselineAssessment.objects.get_or_create(pk=student_id)[0]
    context['student_list'] = Student.objects.all()
    context['tab'] = 'baseline'

    return render(request, template, context)


@login_required(login_url='/login/')
def ILR(request):
    template = 'opencmis/ilr.xml'
    student_list = Student.objects.all()

    context = {'header': Header}
    my_list = []
    for student in student_list:
        item = {'student': student}
        # The next line is GOLD DUST!
        # It return columns from both the StudentQualification and the Qualification tables.
        # Note to access StudentQualification columns use field,
        # to access Qualification columns use qualification.field.
        item['aim_list'] = StudentQualification.objects.filter(student=student.id).select_related('qualification')
        my_list.append(item)
    context['student_list'] = my_list
    return render(request, template, context)


def gmail(request):
    template = 'opencmis/gmail.csv'
    context = {'student_list': Student.objects.all()}
    return render(request, template, context)


class BaselineIndex(ListView):
    model = BaselineValue
    template_name = 'opencmis/baseline.html'
    context_object_name = 'item_list'

    def get_object(self):
        return get_object_or_404(BaselineAssessment, pk=self.kwargs['student_id'])

    def get_context_data(self, **kwargs):
        context = super(BaselineIndex, self).get_context_data(**kwargs)
        context['student_list'] = Student.objects.all()
        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_id'])
        my_list = []
        for entry in BaselineEntry.objects.all():
            item = {'entry': entry}
            item['data'] = BaselineValue.objects.filter(student=self.kwargs['student_id'], baseline=entry).order_by('week')
            my_list.append(item)
        context['baseline_list'] = my_list
        context['tab'] = 'baseline'
        return context

    def get_queryset(self):
        return BaselineValue.objects.filter(student=self.kwargs['student_id'])


class BaselineAdd(CreateView):
    model = BaselineValue
    template_name = 'opencmis/baseline-add.html'
    fields = ['text', 'place']

    def get_object(self):
        return get_object_or_404(BaselineValue, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(BaselineAdd, self).get_context_data(**kwargs)
        context['student_list'] = Student.objects.all()

        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_id'])
        my_list = []
        for entry in BaselineEntry.objects.all():
            item = {'entry': entry}
            item['data'] = BaselineValue.objects.filter(student=self.kwargs['student_id'], baseline=entry).order_by('week')
            my_list.append(item)
        context['baseline_list'] = my_list
        context['header'] = self.kwargs['heading']
        context['tab'] = 'baseline'
        return context
