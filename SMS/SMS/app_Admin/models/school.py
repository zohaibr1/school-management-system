from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from .teacher import Teacher
from .student import Student
#Create your models here.

#School Model
name=models.CharField(max_length=50)
teachers=models.ManyToManyField('Teacher')
students=models.ManyToManyField('Student')