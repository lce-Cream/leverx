from django.urls import path
from courses import views
from .yasg import urlpatterns as docpatterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = []

urlpatterns += docpatterns

urlpatterns += [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('users/', views.CreateUser.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('courses/', views.ListCreateCourse.as_view()),
    path('courses/<int:pk>/', views.CourseDetail.as_view()),

    path('lectures/', views.ListCreateLecture.as_view()),
    path('lectures/<int:pk>/', views.LecuteDetail.as_view()),

    path('tasks/', views.ListCreateTask.as_view()),
    path('tasks/<int:pk>/', views.TaskDetail.as_view()),

    path('grades/', views.ListCreateTask.as_view()),
    path('grades/<int:pk>/', views.GradeDetail.as_view()),
]
