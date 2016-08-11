from django.contrib import admin
from .models import Student, Teacher, Building, Room, Qualification, StudentQualification


from django.contrib import admin
from import_export import resources

from .models import Student

from import_export.admin import ImportExportModelAdmin


# Hopefully add import / export facilities to the admin page
class StudentAdmin(ImportExportModelAdmin):
    pass


# Setup import_export
# See https://django-import-export.readthedocs.io/en/latest/getting_started.html
class StudentResource(resources.ModelResource):

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name',)           # These are the fields I want to import
        export_order = ('id', 'first_name', 'last_name',)     # This is the order for export
        # Let me know what's happening
        skip_unchanged = True
        report_skipped = True

#Mega Important: Will not work until you register StudentAdmin with admin site
admin.site.register(Student, StudentAdmin)


# admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Qualification)
admin.site.register(StudentQualification)
