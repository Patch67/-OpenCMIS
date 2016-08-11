from django.contrib import admin
from .models import Student, Teacher, Building, Room, Qualification, StudentQualification
# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Qualification)
admin.site.register(StudentQualification)
