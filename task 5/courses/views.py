from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import generics

from courses.serializers import GradeSerializer, LectureSerializer, TaskSerializer, UserSerializer, CourseSerializer
from courses import models

# User
class UserList(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer


# Course
class CourseList(generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer


# Lecture
class LectureList(generics.ListCreateAPIView):
    queryset = models.Lecture.objects.all()
    serializer_class = LectureSerializer


class LecuteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Lecture.objects.all()
    serializer_class = LectureSerializer


# Task
class TaskList(generics.ListCreateAPIView):
    queryset = models.Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Task.objects.all()
    serializer_class = TaskSerializer


# Grade
class GradeList(generics.ListCreateAPIView):
    queryset = models.Grade.objects.all()
    serializer_class = GradeSerializer


class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Grade.objects.all()
    serializer_class = GradeSerializer