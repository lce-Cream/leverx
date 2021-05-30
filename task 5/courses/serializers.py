from rest_framework import serializers
from courses.models import User, Course, Lecture, Task, Grade

# User
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'status']
    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            status=validated_data['status'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'status']


# Course
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'owner', 'participants']


# Lecture
class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['subject', 'course', 'presentation', 'homework']


# Task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['lecture', 'author', 'solution']


# Grade
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['value', 'comment', 'recipient', 'task']
