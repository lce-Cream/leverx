from rest_framework import serializers
from courses.models import User, Course, Lecture, Task, Grade


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'group', 'email', 'password']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'owner', 'participants']


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['subject', 'course', 'presentation', 'homework']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['lecture', 'author', 'solution']


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['value', 'comment', 'recipient', 'task']
