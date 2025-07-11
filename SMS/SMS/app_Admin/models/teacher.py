from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from .subject import Subject
from .classroom import Classroom

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id=models.CharField(max_length=50, unique=True, primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    subject=models.ManyToManyField(Subject,related_name="Subjects")
    classroom=models.ManyToManyField(Classroom, related_name="classrooms")
    address=models.TextField()
    contact_no=models.CharField(max_length=11)
    email=models.EmailField(unique=True)
    Join_date=models.DateField()