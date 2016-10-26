from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Student, Status, StudentQualification, Behaviour, Qualification,\
    BaselineValue, BaselineEntry, Header
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import csv
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class IndexView(LoginRequiredMixin, ListView):
    # This view is only accessible to logged in users
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Student
    template_name = 'opencmis/index.html'
    context_object_name = 'student_list'
    permission_required = 'opencmis.view_student'

    def get_context_data(self, **kwargs):
        """Customise the context ready to supply to the template"""
        context = super(IndexView, self).get_context_data(**kwargs)

        # The following two lines should appear in every context
        context['student'] = 'Nobody'
        context['tab'] = ''
        context['index'] = index_context(self.request)
        return context

    def get_queryset(self):
        return Student.objects.all()


class StudentView(DetailView):
    model = Student
    permission_required = 'opencmis.view_student'
    template_name = 'opencmis/detail.html'

    def get_context_data(self, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        context['index'] = index_context(self.request)
        return context


class StudentCreate(CreateView):
    model = Student
    permission_required = 'opencmis.add_student'
    fields = ['status', 'title', 'first_name', 'last_name', 'date_of_birth',
              'gender', 'ethnicity', 'ULN',
              'house', 'road', 'area', 'town', 'post_code']

    def get_object(self):
        return get_object_or_404(Student, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StudentCreate, self).get_context_data(**kwargs)
        context['index'] = index_context(self.request)
        context['student'] = 'Nobody'
        return context


class StudentUpdate(UpdateView):
    model = Student
    permission_required = 'opencmis.change_student'
    fields = ['status', 'title', 'first_name', 'last_name', 'date_of_birth',
              'ethnicity', 'gender', 'ULN',
              'house', 'road', 'area', 'town', 'post_code']

    def get_object(self):
        return get_object_or_404(Student, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(StudentUpdate, self).get_context_data(**kwargs)
        context['index'] = index_context(self.request)
        return context


class StudentDelete(DeleteView):
    model = Student
    permission_required = 'opencmis.delete_student'
    success_url = reverse_lazy('opencmis:index')

    def get_context_data(self, **kwargs):
        context = super(StudentDelete, self).get_context_data(**kwargs)
        context['index'] = index_context(self.request)
        return context


class StudentQualificationList(ListView):
    model = StudentQualification
    template_name = 'opencmis/qualification_index.html'
    context_object_name = 'qual_list'

    def get_context_data(self, **kwargs):
        """Customise the context ready to supply to the template"""
        context = super(StudentQualificationList, self).get_context_data(**kwargs)
        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_id'])
        context['tab'] = 'qualification'
        context['index'] = index_context(self.request)
        return context

    def get_queryset(self):
        # Get the student id from the key word arguments and filter the related quals
        return StudentQualification.objects.filter(student=self.kwargs['student_id'])


class StudentQualificationAdd(CreateView):
    model = StudentQualification
    fields = ['qualification', 'start', 'expected_end']

    def get_object(self):
        return get_object_or_404(StudentQualification, pk=self.kwargs['studentqualification_id'])

    def get_context_data(self, **kwargs):
        context = super(StudentQualificationAdd, self).get_context_data(**kwargs)
        context['index'] = index_context(self.request)
        context['tab'] = 'qualification'
        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_id'])
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
    context['index'] = index_context(request)
    return render(request, template, context)


def gmail(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Gmail_batch.csv"'

    student_list = Student.objects.all()
    writer = csv.writer(response)
    writer.writerow(['first name', 'last name', 'email', 'password'])
    for student in student_list:
        writer.writerow([student.first_name, student.last_name,
                         '{0}.{1}@cscd.ac.uk'.format(student.first_name.lower(), student.last_name.lower()),
                         "password"])

    return response


@login_required(login_url='/login/')
def ILR(request):
    student_list = Student.objects.all()

    context = {'header': Header}
    my_list = []
    for student in student_list:
        item = {'student': student}
        # TODO: Best practice: How to filter over multiple joined tables
        # The next line is GOLD DUST!
        # It return columns from both the StudentQualification and the Qualification tables.
        # Note to access StudentQualification columns use field,
        # to access Qualification columns use qualification.field.
        item['aim_list'] = StudentQualification.objects.filter(
            student=student.id).select_related('qualification')
        my_list.append(item)
    context['student_list'] = my_list
    # Set up response as a file download
    response = HttpResponse(content_type='text/xml')
    # TODO: Make the IRL filename the correct format
    response['Content-Disposition'] = 'attachment; filename="ilr.xml"'
    t = loader.get_template('opencmis/ilr.xml')

    response.write(t.render(context))
    return response


class BaselineIndex(ListView):
    model = BaselineValue
    template_name = 'opencmis/baseline.html'
    context_object_name = 'item_list'

    def get_context_data(self, **kwargs):
        context = super(BaselineIndex, self).get_context_data(**kwargs)
        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_id'])
        my_list = []
        for entry in BaselineEntry.objects.all():
            item = {'entry': entry}
            item['data'] = BaselineValue.objects.filter(student=self.kwargs['student_id'],
                                                        baseline=entry).order_by('week')
            my_list.append(item)
        context['baseline_list'] = my_list
        context['tab'] = 'baseline'
        context['index'] = index_context(self.request)
        return context

    def get_queryset(self):
        return BaselineValue.objects.filter(student=self.kwargs['student_id'])


class BaselineAdd(CreateView):
    model = BaselineValue
    template_name = 'opencmis/baseline-add.html'
    fields = ['text']

    def get_object(self):
        return get_object_or_404(BaselineValue, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(BaselineAdd, self).get_context_data(**kwargs)

        context['student'] = get_object_or_404(Student, pk=self.kwargs['student_id'])
        my_list = []
        for entry in BaselineEntry.objects.all():
            item = {'entry': entry}
            item['data'] = BaselineValue.objects.filter(student=self.kwargs['student_id'], baseline=entry).order_by('week')
            my_list.append(item)
        context['baseline_list'] = my_list
        context['header'] = self.kwargs['heading']
        context['tab'] = 'baseline'
        context['index'] = index_context(self.request)
        return context


# KPI Section
def make_alert(low, medium, high, value):
    """
    Calculates the alert level according to the following parameters.
    This is used to categorize the Bootstrap CSS controls
    :param lo: Any value lower than low will return a danger alert
    :param medium: Any other value lower than medium will return a warning alert
    :param high: Any other value lower than high will return an info alert
    :param value: Any other value will produce a success alert
    :return:
    """
    if value < low:
        alert = 'danger'
    elif value < medium:
        alert = 'warning'
    elif value < high:
        alert = 'info'
    else:
        alert = 'success'
    return alert


def percentage(value, total):
    return int(100 * value / total)


def make_kpi(title, total, number, text):
    percent = percentage(number, total)
    kpi = {'title': title,
           'is_progress_bar': True,
           'total': total,
           'number': number,
           'percent': percent,
           'text': text,
           'alert': make_alert(25, 50, 75, percent)}
    return kpi


@login_required()
def dashboard(request):
    template = 'opencmis/dashboard.html'

    # This is where the key performance indicators go
    student_numbers = Student.objects.count()

    # Baseline Assessment KPI
    baseline_possible = Student.objects.count() * BaselineEntry.objects.count() * 6
    baseline_actual = BaselineValue.objects.count()
    baseline_kpi = make_kpi("Baseline Assessment", baseline_possible, baseline_actual,
                            "students have a valid Baseline Assessment")

    # Qualification KPI
    number = StudentQualification.objects.values_list('student', flat=True).distinct().count()
    qualification_kpi = make_kpi("Student Qualification", student_numbers, number,
                                 "students have any qualifications set")

    # Make list of dictionaries, ready to pass to the template
    kpi_list = [
        baseline_kpi,
        qualification_kpi,
        make_kpi("Patrick", 100, 74, "target have been achieved"),
        make_kpi("Ramzan", 100, 100, "targets have been achieved."),
        make_kpi("Warning", 100, 30, "somethings not good enough")
    ]

    # Put the list in a dictionary context, add user as another top level dictionary item so it can be displayed on page
    context = {'kpi_list': kpi_list, 'user': request.user}

    return render(request, template, context)


def index_context(request):
    """index filtering"""

    # TODO Make this Ajax and you're cooking on gas baby
    # TODO: Make the search form remember the value of the previous search items, at least the Drop Box

    # Check to see if index is limited via Filter
    f = request.GET.get('filter')
    if not f or f == 'any':
        index = Student.objects.all().order_by('first_name')
    else:
        index = Student.objects.filter(status=f).order_by('first_name')
    # Check to see if index is limited via search
    query = request.GET.get('q')
    if query:
        query_list = query.split()
        if len(query_list) == 1:
            # TODO: Awesome example of filtering over multiple fields using filters and Q objects
            # Note: first_name__contains translates to SQL like for a sloppy text search
            # If there is only one search term it could be a fragment of first_name or last_name
            index = index.filter(Q(first_name__contains=query_list[0]) | Q(last_name__contains=query_list[0]))
        elif len(query_list) == 2:
            # if there are two search terms the first one must be first_name and the second last_name
            index = index.filter(Q(first_name__contains=query_list[0]) | Q(last_name__contains=query_list[1]))
    # TODO: Best Practice Do indices like this with pagination
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
    # Make dictionary containing the index and the filter values
    d = {'index': index}
    d['filter'] = Status.objects.all()
    return d
