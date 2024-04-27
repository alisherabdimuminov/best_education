from django.urls import path

from .views import (
    login,
    signup,
    logout,
    change_data,
    change_password,
    students,
    student,
    teachers,
    teacher
)

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    path("change_data/", change_data, name="change_data"),
    path("change_password/", change_password, name="change_password"),
    path("students/", students, name="students"),
    path("students/students/<int:pk>/", student, name="student"),
    path("teachers/", teachers, name="teachers"),
    path("teacher/teacher/<int:pk>/", teacher, name="teacher"),
]
