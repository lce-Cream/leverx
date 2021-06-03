from rest_framework import permissions
from courses.models import Course, User, Lecture, Grade, Task

class AllowAny(permissions.BasePermission):
    def has_permission(self, request, view):
        return True


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.status == 'teacher'


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.status == 'student'


class IsTaskOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.id


class IsCourseMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.get_view_name() == 'Course Detail':
            course = Course.objects.get(id=request.data['course'])
            return course.participants.filter(id=request.user.id).exists()

        elif view.get_view_name() in ('List Create Lecture', 'Lecture Detail'):
            course = Course.objects.get(id=request.data['course'])
            return course.participants.filter(id=request.user.id).exists()

        elif view.get_view_name() in ('Create Task', 'Task Detail'):
            lecture = Lecture.objects.get(id=request.data['lecture'])
            course = Course.objects.get(id=lecture.course.id)
            return course.participants.filter(id=request.user.id).exists()

        elif view.get_view_name() in ('Create Grade', 'Grade Detail'):
            task = Task.objects.get(id=request.data['task'])
            lecture = Lecture.objects.get(id=task.lecture.id)
            course = Course.objects.get(id=lecture.course.id)
            return course.participants.filter(id=request.user.id).exists()
