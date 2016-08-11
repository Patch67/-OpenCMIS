from django.contrib import admin
from .models import Student, Teacher, Building, Room, Qualification, StudentQualification


from django.contrib import admin
from import_export import resources
from .models import Student
from import_export.admin import ImportExportModelAdmin


# Student import_export
class StudentAdmin(ImportExportModelAdmin):
    pass


class StudentResource(resources.ModelResource):

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name',)           # These are the fields I want to import
        export_order = ('id', 'first_name', 'last_name',)     # This is the order for export
        # Let me know what's happening
        skip_unchanged = True
        report_skipped = True


# Qualification import_export
class QualificationAdmin(ImportExportModelAdmin):
    pass


class QualificationResource(resources.ModelResource):

    class Meta:
        model = Qualification
        fields = ('title', 'LAR',)             # Fields to import. NB. Will always want id in column 1
        export_order = ('id', 'title', 'LAR',) # Fields to export
        # Let me know what's happening
        skip_unchanged = True
        report_skipped = True


# Building import_export
class BuildingAdmin(ImportExportModelAdmin):
    pass


class BuildingResource(resources.ModelResource):
    class Meta:
        model = Building
        fields = ('name', )  # Fields to import. NB. Will always want id in column 1
        export_order = ('id', 'name', )  # Fields to export
        # Let me know what's happening
        skip_unchanged = True
        report_skipped = True


# Room import_export
class RoomAdmin(ImportExportModelAdmin):
    pass


class RoomResource(resources.ModelResource):
    class Meta:
        model = Room
        fields = ('building', 'number', 'name',)  # Fields to import. NB. Will always want id in column 1
        export_order = ('id', 'building', 'number', 'name',)  # Fields to export
        # Let me know what's happening
        skip_unchanged = True
        report_skipped = True


# See https://django-import-export.readthedocs.io/en/latest/getting_started.html
# Import_export will not work until you register StudentAdmin with admin site
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(StudentQualification)

'''
Notes
-----
When importing tables that have foreign keys life can get tricky, especially if your source data does not export IDs.

The solution I found was to use Excel as an intermediary.
1) Import the parent table into excel.  Generate your own IDs - simple numbers 1,2,3, etc.
2) Import the child table with the text field of the parent table and the other fields.
3) Use the Excel Vlookup function to match the text field of the parent table with your ID in the parent table.
4) Copy the entire lot and use paste as values into a new spreadsheet.
5) Chop and change the columns as you need to fit your new django import order
6) Export as Tab Separated Value and import into Django as tsb.

Also note that Django import expects dates to be in US format.
So again in Excel you can format the dates as US then copy and paste values then export that.
'''
