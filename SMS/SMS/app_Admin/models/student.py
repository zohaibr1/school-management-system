from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from .teacher import Teacher
from .classroom import Classroom
from .subject import Subject
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    id=models.CharField(max_length=250, primary_key=True)
    first_name=models.CharField(max_length=250)
    last_name=models.CharField(max_length=250)
    classroom=models.ForeignKey(Classroom, on_delete=models.CASCADE)
    address=models.TextField()
    teacher=models.ManyToManyField(Teacher, related_name="teachers")
    subject=models.ManyToManyField(Subject,related_name="subjects")
    email=models.EmailField(unique=True, default='@')
    contact_no=models.CharField(max_length=11, default='XXXXXXXXXXX')
    def __str__(self):
        return f'{self.first_name}{self.last_name}{self.classroom}' 
    