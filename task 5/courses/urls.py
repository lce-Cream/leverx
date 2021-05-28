from django.urls import path, include
from rest_framework import routers
from courses import views


urlpatterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path('courses/', views.CourseList.as_view()),
    path('courses/<int:pk>/', views.CourseDetail.as_view()),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('lectures/', views.LectureList.as_view()),
    path('lectures/<int:pk>/', views.LecuteDetail.as_view()),

    path('tasks/', views.TaskList.as_view()),
    path('tasks/<int:pk>/', views.TaskDetail.as_view()),

    path('grades/', views.GradeList.as_view()),
    path('grades/<int:pk>/', views.GradeDetail.as_view()),
]
