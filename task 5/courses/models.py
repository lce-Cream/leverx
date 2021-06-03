from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    status = models.CharField(max_length=10, choices=[('student', 'student'), ('teacher', 'teacher')])


class Course(models.Model):
    title = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return str(self.title)


class Lecture(models.Model):
    subject = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    presentation = models.FileField(blank=True)
    homework = models.TextField()
    
    def __str__(self):
        return str((self.subject, self.course))


class Task(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    solution = models.CharField(max_length=100)

    def __str__(self):
        return str((self.lecture, self.author))


class Grade(models.Model):
    value = models.IntegerField()
    comment = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return str((self.value, self.task))
