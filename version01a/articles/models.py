from django.db import models


class Article(models.Model):
    """
    This is pretty good example of a model and could be used as a template for others.
    """
    # TODO: Look at the model fields to see if they have the correct null=True or False parameters
    title = models.CharField(max_length=80, blank=False)
    author = models.CharField(max_length=12, blank=False)
    tags = models.CharField(max_length=100, blank=False)
    body = models.TextField(blank=False)
    date = models.DateTimeField(auto_now_add=True)  # TODO: Should this be auto_add_now or auto_add_now_other?
    archive = models.BooleanField(default=False)

    def __str__(self):
        """
        This function return a string that can be used to identify an individual object
        :return:
        """
        return "%s by %s" % (self.title, self.author)

    def get_absolute_url(self):
        """
        This function return the URL of that can be used to view an individual object
        :return:
        """
        return u'/article/%d/' % self.id

# TODO: Should a define a form for this model and should it be done here?

