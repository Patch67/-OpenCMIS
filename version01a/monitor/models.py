from django.db import models


class Device(models.Model):
    ip_address = models.CharField(max_length=16)
    url = models.CharField(max_length=120)
    ping_ip = models.BooleanField()
    ping_url = models.BooleanField()
    test_url = models.BooleanField()


