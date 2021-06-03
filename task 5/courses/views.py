from rest_framework.response import Response
from rest_framework import generics, status
from .permissions import *
from .serializers import *
from . import models

# User
class CreateUser(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = models.User.objects.all()
    serializer_class = CreateUserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (ReadOnly | IsAccountOwner,)
    queryset = models.User.objects.all()
    serializer_class = ViewUserSerializer


# Course
class ListCreateCourse(generics.ListCreateAPIView):
    permission_classes = (ReadOnly | IsTeacher,)
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                'title': request.data['title'],
                'participants': [request.user.id],
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (ReadOnly | IsTeacher & IsCourseMember,)
    queryset = models.Course.objects.all()
    serializer_class = CourseSerializer


# Lecture
class ListCreateLecture(generics.ListCreateAPIView):
    permission_classes = (ReadOnly | IsTeacher & IsCourseMember,)
    queryset = models.Lecture.objects.all()
    serializer_class = CreateLectureSerializer


class LectureDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (ReadOnly | IsTeacher & IsCourseMember,)
    queryset = models.Lecture.objects.all()
    serializer_class = ViewLectureSerializer


# Task
class CreateTask(generics.CreateAPIView):
    permission_classes = (IsCourseMember,)
    queryset = models.Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data={
                'lecture': request.data['lecture'],
                'solution': request.data['solution'],
                'author': request.user.id,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsTaskOwner | IsTeacher & IsCourseMember,)
    queryset = models.Task.objects.all()
    serializer_class = TaskSerializer


# Grade
class CreateGrade(generics.CreateAPIView):
    permission_classes = (IsTeacher & IsCourseMember,)
    queryset = models.Grade.objects.all()
    serializer_class = GradeSerializer


class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ((ReadOnly & IsStudent & IsCourseMember) | (IsCourseMember & IsTeacher),)
    queryset = models.Grade.objects.all()
    serializer_class = GradeSerializer