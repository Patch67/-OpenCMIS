from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Issue(models.Model):
    title = models.CharField(max_length=120, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.TextField()
    PRIORITY_CHOICES = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'))
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    SPEED_CHOICES = (('Q', 'Quick'), ('M', 'Medium'), ('S', 'Slow'))
    speed = models.CharField(max_length=1, choices=SPEED_CHOICES, default='M')
    STATUS_CHOICES = (('O', 'Open'), ('C', 'Closed'), ('H', 'On hold'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='O')
    creation_time = models.DateTimeField(default=timezone.now)
    response_time = models.DateTimeField(null=True, blank=True)
    complete_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('issue:detail', kwargs={'pk': str(self.pk)})


class Update(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now)
    personnel = models.ForeignKey(User, on_delete=models.CASCADE)
    update = models.TextField()

    def __str__(self):
        return '{0} {1}'.format(self.date, self.personnel)

    def get_absolute_url(self):
        # Default page is details page of the parent issue
        return reverse('issue:detail', kwargs={'pk': str(self.issue)})

    def save(self, *args, **kwargs):
        # TODO: Investigate save method as the place to do logging
        # Do something before saving
        super(Update, self).save(*args, **kwargs)
        # Do something after saving
