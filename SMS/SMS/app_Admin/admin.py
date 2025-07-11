from django.contrib import admin
from app_Admin.models import Student,Teacher,Subject, Classroom,Attendance
# Register your models here.
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Classroom)
admin.site.register(Attendance)
