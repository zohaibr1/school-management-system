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

#teacher dashboard


class teacherDashboardView(View):
    def get(self,request):
        user = request.user  

        try:
            teacher = Teacher.objects.prefetch_related('classroom', 'subject').get(user=user)
        except Teacher.DoesNotExist:
            teacher = None
        announcements = Announcement.objects.filter(uploader=teacher).order_by('-id')[:5] if teacher else []

        students = Student.objects.filter(teacher=teacher).distinct() if teacher else []

        attendance_records = Attendance.objects.filter(teacher=teacher).order_by('-date')[:5] if teacher else []

        context = {
            'teacher': teacher,
            'subjects': teacher.subject.all() if teacher else [],
            'classrooms': teacher.classroom.all() if teacher else [],
            'students': students,
            'announcements': announcements,
            'attendance_records': attendance_records,
        }

        return render(request, 'dashboard_teachers.html', context)
    

        #Students list

#student list in teacher dashboard
class assignStudents(View):
    def get(self,request):
        teacher=Teacher.objects.get(user=request.user)
        classrooms=teacher.classroom.all()
        selected_class=request.GET.get('classroom')
        if selected_class:
            students = Student.objects.filter(classroom_id=selected_class, teacher=teacher)
        else:
            students = Student.objects.filter(classroom__in=classrooms, teacher=teacher)
        return render(request, 't_students.html',{'select_classroom':selected_class, 'students':students,'classrooms':classrooms })
#make announcement
class makeAnnouncemeent(View):
    def get(self,request):
        form=AnnouncementForm()
        teacher = Teacher.objects.get(user=request.user)
        announcements = Announcement.objects.filter(uploader=teacher).order_by('-created_at')
        return render(request, 't_announcements.html', {'form': form, 'announcements': announcements})
    def post(self,request):
        teacher = Teacher.objects.get(user=request.user)
        if request.method == 'POST':
            form = AnnouncementForm(request.POST)
            if form.is_valid():
                ann = form.save(commit=False)
                ann.uploader = teacher
                ann.save()
                form.save_m2m()
                messages.success(request, "Announcement posted successfully!")
                return redirect('t_announcements')
        else:
            form = AnnouncementForm()

#mark attendance
class markAttendance(View):
    
    def get(self,request):
        teacher = Teacher.objects.get(user=request.user)
        classrooms = teacher.classroom.all()
    
        selected_classroom_id = request.GET.get('classroom')
        students = Student.objects.filter(classroom__in=classrooms)

        if selected_classroom_id:
            students = students.filter(classroom__id=selected_classroom_id)

        return render(request, 't_attendance.html', {
        'students': students,
        'classrooms': classrooms,
        
    })
    def post(self,request):
        teacher = Teacher.objects.get(user=request.user)
        classrooms = teacher.classroom.all()

        selected_classroom_id = request.GET.get('classroom')
        students = Student.objects.filter(classroom__in=classrooms)

        if selected_classroom_id:
            students = students.filter(classroom__id=selected_classroom_id)
        today = timezone.now().date()

        for student in students:
            status = request.POST.get(f'attendance_{student.id}')
            Attendance.objects.update_or_create(
                    teacher=teacher,
                    student=student,
                    date=today,
                    defaults={'attendance': status, 'teacher': teacher}
                )
            return redirect('t_attendance')


#delete ana announcement

class deleteAnnouncemment(View):
    def get(self,request,ann_id):
        teacher=get_object_or_404(Teacher,user=request.user)
        ann = get_object_or_404(Announcement, id=ann_id, uploader=teacher)
        return render(request,'delete_announcement.html',{'announcement': ann})
    def post(self,request,ann_id):
        teacher=get_object_or_404(Teacher,user=request.user)
        ann = get_object_or_404(Announcement, id=ann_id, uploader=teacher)
        ann.delete()
        messages.success(request, "Announcement deleted.")
        return redirect('t_announcements')