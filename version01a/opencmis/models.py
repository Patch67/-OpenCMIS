from django.db import models
from django.core.urlresolvers import reverse


class Student(models.Model):
    gender_choices = (('M', 'Male'), ('F', 'Female'))
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=30, null=False)
    gender = models.CharField(max_length=1, choices=gender_choices, default='M')
    date_of_birth = models.DateField(null=True)
    ULN = models.CharField(max_length=10, null=True)
    house = models.CharField(max_length=50, null=True)
    road = models.CharField(max_length=50, null=True)
    area = models.CharField(max_length=50, null=True)
    town = models.CharField(max_length=50, null=True)
    post_code = models.CharField(max_length=12, null=True)
    photo = models.FileField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('opencmis:detail', kwargs={'pk': self.pk})


class Teacher(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=30, null=False)
    role = models.CharField(max_length=30, null=False)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Qualification(models.Model):
    title = models.CharField(max_length=100, null=False)
    LAR = models.CharField(max_length=12, null=False)

    def __str__(self):
        return '%s: %s' % (self.LAR, self.title)


class StudentQualification(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    qualification = models.ForeignKey('Qualification', on_delete=models.CASCADE)
    start = models.DateField(null=False)
    expected_end = models.DateField(null=False)

    def __str__(self):
        return '%s: %s' % (self.student, self.qualification)


class Building(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % self.name


class Room(models.Model):
    building = models.ForeignKey('Building', on_delete=models.CASCADE)
    room = models.CharField(max_length=20, null=False)


def __str__(self):
    return '%s: %s' % (self.building, self.name)




