from django.contrib.auth.models import User
from django.db import models

"""
This application manages the shared document within our organisation.
It is designed to replace Moodle (in the sense that Moodle is used as an intranet).

It provides the means for each organisation to define sections with each section
having a number of entries.
(* What about sub-sections ?*)

Each section can have multiple entries.  Each entry relates to a specific document.
Each section also has a unique position field which allows the order of the fields
to be defined.

Each entry may actually have a number of files associated with it.  Each of these files
is actually a version.
Each entry has a person_responsible field and a next_review date field.  This allows the
system to generate alerts, either in-system alerts or email alerts to remind the
person_responsible to review and/or update the document.

There should also be a key performance indicator to show the state of our documents, i.e.
the percentage of documents which are up to date.
"""


class Review(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()


class Document(models.Model):
    """
    A document is a filename and a title.
    Note the actual filename is auto-generated and will not be the same as the user given
    filename.
    """
    file_name = models.CharField(max_length=256, null=False)
    title = models.CharField(max_length=80, null=False)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


class DocumentReview(models.Model):
    """
    This provides a history of reviews for a document
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)


class Organisation(models.Model):
    """
    Trust, Nursery, School, College, SES, whatever...
    """
    ORGANISATION_CHOICES = (('Tru', 'Trust'), ('Nur', 'Nursery'), ('Sch', 'School'),
                            ('Col', 'College'), ('SES','Specialist Employment Service'))
    organisation = models.CharField(max_length=3, null=False)


class Section(models.Model):
    """
    Section heading for each organisation
    """
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    section = models.CharField(max_length=120, null=False)


class Entry(models.Model):
    """
    Each section may contain multiple Entries.
    Each entry contains an entry and a section to which it belongs.
    Each entry also has a unique position with the section, i.e. 0,1,2,3,4, etc.
    This is used to define the order will will allow orders to be altered.
    Finally the entry contains a link to the Policy record.

    Note that this schema does not account for any policy version history.
    It might be an idea to have another table to define a history to changes can be tracked.
    """
    entry = models.CharField(max_length=120)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    position = models.IntegerField(unique=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)

    # The following booleans are used to define who the policy applies to.
    # In this way users can be presented with the correct policies fro them.
    school_staff = models.BooleanField(default=True)
    school_pupils = models.BooleanField(default=True)

    college_staff = models.BooleanField(default=True)
    college_students = models.BooleanField(default=True)

    nursery_staff = models.BooleanField(default=True)
    nursery_children = models.BooleanField(default=True)

    trust_staff = models.BooleanField(default=True)


"""
How will this work in practice?
Trust will have a set of policies that apply to everyone unless they are overrules by a sub policy.
By default Trust policies will only refer to staff.
College will have a number of sections ...
- Policies
- Quality Assurance
-
"""