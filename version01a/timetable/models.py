from django.db import models
"""
Patrick Notes
-------------
Every value in the database should have a history.
Starting with when it was created, through all it's updates,
concluding with it's deletion.
Each entry should have the user and the date/time and also
the previous value and new value.
There should be a mechanism on each field to view the history and
to revert to a previous value.
"""

day_choices = (('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'),
               ('Thu', 'Thursday'), ('Fri', 'Friday'),
               ('Sat', 'Sunday'), ('Sun', 'Sunday'))

status_choices = (('Active', 'Active'), ('Archived', 'Archived'))


class Subject(models.Model):
    subject = models.CharField(max_length=20)
    status = models.CharField(choices=status_choices, max_length=8)
    colour =models.CharField(max_length=6, blank=True)

    def __str__(self):
        return '%s' % self.subject


class SessionTemplate(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    day = models.CharField(choices=day_choices, max_length=3)
    time = models.TimeField()
    duration = models.IntegerField()



