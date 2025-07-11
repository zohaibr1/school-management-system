from django.views import View
from django.shortcuts               import render, redirect, get_object_or_404
from django.http                    import HttpResponse
from django.contrib.auth.models     import User
from django.contrib.auth            import authenticate, login as auth_login
from django.contrib.auth.views      import LoginView
from app_Admin.forms                 import TeacherForm, StudentForm,AnnouncementForm
from django.contrib                 import messages
from app_Admin.models               import Teacher, Student,Classroom, Attendance, Announcement, Subject
from django.contrib.auth.decorators import login_required
from datetime                       import datetime
from django.core.exceptions         import ValidationError
from django.views.decorators.http   import require_POST
from datetime                       import date
from django.utils                   import timezone

#dashboard of student
class studentDashboard(View):
    def get(self,request):
        user = request.user
        try:
            student = Student.objects.select_related('classroom').prefetch_related('subject', 'teacher').get(user=user)
        except Student.DoesNotExist:
            student = None

        attendance_records = Attendance.objects.filter(student=student).order_by('-date')[:5]  # last 5 records
        announcements = Announcement.objects.all().order_by('-created_at')[:5]

        context = {
            'student': student,
            'subjects': student.subject.all() if student else [],
            'teachers': student.teacher.all() if student else [],
            'attendance_records': attendance_records,
            'announcements': announcements,
        }

        return render(request, 'dashboard_students.html', context)
    
#Announcement View
class announcementView(View):
    def get(self,request):
        user = request.user
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            student = None
        announcements = []
        if student:
            classrooms = [student.classroom]  
            assigned_teachers = student.teacher.all()
            announcements = Announcement.objects.filter(tragetClass=student.classroom,uploader__in=assigned_teachers ).order_by('-created_at')
        return render(request, 's_announcements.html', {
        'announcements': announcements
        })
    
#Announcement view students
class anttendanceView(View):
    def get(self,request):
        user=request.user
        try:
            student=Student.objects.get(user=user)
        except Student.DoesNotExist:
            student=None
        attendance_records = Attendance.objects.filter(student=student).order_by("-date")
        return render(request, 's_Attendance.html',{'attendance_records': attendance_records,})
            