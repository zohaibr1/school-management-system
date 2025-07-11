from django import forms
from .models import Teacher,Student, Announcement 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TeacherForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        # filter only users not already assigned to a student
        assigned_student_users = Student.objects.values_list('user_id', flat=True)
        assigned_teacher_users = Teacher.objects.values_list('user_id', flat=True)
        all_assigned_users = list(assigned_student_users) + list(assigned_teacher_users)
    # Filter: only regular users, not assigned to a student, not admin/staff
        self.fields['user'].queryset = User.objects.filter(
        is_superuser=False,
        is_staff=False
        ).exclude(id__in=all_assigned_users)

    # Optional: add Bootstrap class
        self.fields['user'].widget.attrs.update({'class': 'form-select'})
#Student Creation form
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        # filter only users not already assigned to a student
        assigned_student_users = Student.objects.values_list('user_id', flat=True)
        assigned_teacher_users = Teacher.objects.values_list('user_id', flat=True)
        all_assigned_users = list(assigned_student_users) + list(assigned_teacher_users)
    # Filter: only regular users, not assigned to a student, not admin/staff
        self.fields['user'].queryset = User.objects.filter(
        is_superuser=False,
        is_staff=False
        ).exclude(id__in=all_assigned_users)

    # Optional: add Bootstrap class
        self.fields['user'].widget.attrs.update({'class': 'form-select'})

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'tragetClass']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['tragetClass'].widget.attrs['multiple'] = True