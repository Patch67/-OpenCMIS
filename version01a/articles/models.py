from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=80, blank=False)
    author = models.CharField(max_length=12, blank=False)
    tags = models.CharField(max_length=100, blank=False)
    body = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return "%s by %s" % (self.title, self.author)

    def get_absolute_url(self):
        return u'/article/%d/' % self.id
