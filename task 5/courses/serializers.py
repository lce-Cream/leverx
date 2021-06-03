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
        fields = ['id', 'username', 'email', 'status', 'date_joined']



class CourseSerializer(serializers.ModelSerializer):
    # participants = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')
    class Meta:
        model = Course
        fields = ['id', 'participants', 'title']


# Lecture
class CreateLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['id', 'subject', 'course', 'presentation', 'homework']


class ViewLectureSerializer(serializers.ModelSerializer):
    course = serializers.SlugRelatedField(read_only=True, slug_field='title')
    class Meta:
        model = Lecture
        fields = ['id', 'subject', 'course', 'presentation', 'homework']


# Task
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'lecture', 'author', 'solution']


# Grade
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['value', 'comment', 'recipient', 'task']
