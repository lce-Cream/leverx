from django.contrib import admin
from courses.models import *

admin.site.site_header = 'online courses administration'
admin.site.site_title = 'admin'
admin.site.index_title = 'courses'

admin.site.register(User)
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('name', 'group', 'email', 'password')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('subject', 'course', 'presentation', 'homework')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('lecture', 'author', 'solution')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('value', 'comment', 'recipient', 'task')