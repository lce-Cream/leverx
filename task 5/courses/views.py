from courses import models
from rest_framework import generics
from .permissions import *
from .serializers import *

# User
class CreateUser(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = models.User.objects.all()
    serializer_class = CreateUserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = models.User.objects.all()
    serializer_class = ViewUserSerializer


# Course
class ListCreateCourse(generics.ListCreateAPIView):
    permission_classes = (IsTeacherOrReadOnly,)
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer


# Lecture
class ListCreateLecture(generics.ListCreateAPIView):
    permission_classes = (IsTeacherOrReadOnly,)
    queryset = models.Lecture.objects.all()
    serializer_class = LectureSerializer


class LecuteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Lecture.objects.all()
    serializer_class = LectureSerializer


# Task
class ListCreateTask(generics.ListCreateAPIView):
    permission_classes = (IsTeacherOrReadOnly,)
    queryset = models.Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Task.objects.all()
    serializer_class = TaskSerializer


# Grade
class ListCreateGrade(generics.ListCreateAPIView):
    permission_classes = (IsTeacherOrReadOnly,)
    queryset = models.Grade.objects.all()
    serializer_class = GradeSerializer


class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsTeacherOrReadOnly,)
    queryset = models.Grade.objects.all()
    serializer_class = GradeSerializer