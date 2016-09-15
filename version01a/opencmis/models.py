from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Student(models.Model):
    status = models.ForeignKey('Status', blank=False)
    title = models.ForeignKey('Title', blank=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    gender_choices = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(max_length=1, choices=gender_choices, default='M')
    ethnicity = models.ForeignKey('Ethnicity', blank=True, null=True, on_delete=models.SET_NULL)
    date_of_birth = models.DateField(blank=False)
    ULN = models.CharField(max_length=10, blank=True)
    house = models.CharField(max_length=50, blank=True)
    road = models.CharField(max_length=50, blank=True)
    area = models.CharField(max_length=50, blank=True)
    town = models.CharField(max_length=50, blank=True)
    post_code = models.CharField(max_length=12, blank=True)
    photo = models.FileField(blank=True)

    def __str__(self):
        """ return name of an individual object """
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        """
        Return url of an individual object.
        This is used as a follow up address after an editing view has been submitted
         """
        # Although the manual says do it like below it doesn't actually work on my project
        # return reverse('opencmis.views.detail', args=[str(self.id)])
        return u'/opencmis/student/%d' % self.id


class StudentExtras(models.Model):
    student = models.OneToOneField('Student', on_delete=models.CASCADE, primary_key=True)
    NI_number = models.CharField(max_length=12)
    Sexuality = models.CharField(max_length=20, default='Heterosexual')

    def __str__(self):
        return self.student


class Behaviour(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    issue = models.TextField(max_length=50, blank=False)
    action = models.TextField(max_length=50)

    def __str__(self):
        return self.issue


class Teacher(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    role = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Qualification(models.Model):
    title = models.CharField(max_length=100, blank=False)
    LAR = models.CharField(max_length=12, blank=False)

    def __str__(self):
        return '%s: %s' % (self.LAR, self.title)


class StudentQualification(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    qualification = models.ForeignKey('Qualification', on_delete=models.CASCADE)
    start = models.DateField(blank=False)
    expected_end = models.DateField(blank=False)

    def __str__(self):
        return '%s: %s' % (self.student, self.qualification)

    def get_absolute_url(self):
        return u'/opencmis/student/%d/qualification/' % self.student_id


class BaselineEntry(models.Model):
    heading = models.CharField(max_length=80)
    blurb = models.TextField()

    def __str__(self):
        return "%s" %self.heading

    class Meta:
        verbose_name_plural = 'BaselineEntries'


class BaselineValue(models.Model):
    student = models.ForeignKey('Student')
    baseline = models.ForeignKey('BaselineEntry')
    week_choices = ((1, 'Week 1'), (2, 'Week 2'), (3, 'Week 3'), (4, 'Week 4'), (5, 'Week 5'), (6, 'Week 6'))
    week = models.IntegerField(choices=week_choices, default=1)
    text = models.TextField()
    place = models.CharField(max_length=20)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s : week %d" % (self.student, self.baseline, self.week)


    def get_absolute_url(self):
        return u'/opencmis/student/%d/baseline/' % self.student_id


class BaselineAssessment(models.Model):
    """ A one to one record allowing extra details to be added to basic student"""
    student = models.OneToOneField('Student', on_delete=models.CASCADE, primary_key=True)
    blurb = models.TextField(blank=True)
    text = models.TextField(blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return "%s : %s" %(self.student, self.date)


class Building(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.name


class Room(models.Model):
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    room = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return '%s: %s' % (self.building, self.name)


class Staff(models.Model):
    """This is an example of how to make the plural of a class name
    When adding an s simply doesn't cut it."""
    class Meta:
        verbose_name_plural = 'Staff'

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


# Classes for ILR
class Header:
    UKPRN = '10002006'
    post_code = 'DN2 6AY'


class Ethnicity(models.Model):
    value = models.CharField(max_length=30)

    def __str__(self):
        return self.value


class Status(models.Model):
    status = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Status'

    def __str__(self):
        return self.status


class Title(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Titles'

    def __str__(self):
        return self.title
