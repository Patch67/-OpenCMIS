from django.db import models


class Issue(models.Model):
    title = models.CharField(max_length=120, blank=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE())
    summary = models.TextField()
    PRIORITY_CHOICES = ('High', 'Medium', 'Low')
    priority = models.CharField(choices=PRIORITY_CHOICES, default='Medium')
    SPEED_CHOICES = ('Quick', 'Medium', 'Long')
    speed = models.CharField(choices=SPEED_CHOICES, default='Medium')
    creation_time = models.DateTimeField()
    response_time = models.DateTimeField()
    complete_time = models.DateTimeField()

    def __str__(self):
        return self.title