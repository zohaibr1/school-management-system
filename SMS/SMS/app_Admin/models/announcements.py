from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from .subject import Subject
from .classroom import Classroom
from .teacher import Teacher

class Announcement(models.Model):
    title=models.CharField( max_length=200)
    content=models.TextField()
    uploader=models.ForeignKey(Teacher, on_delete=models.CASCADE)
    tragetClass=models.ManyToManyField(Classroom, related_name="Classroom")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title