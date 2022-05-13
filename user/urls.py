
from os import name
from re import template
from django.urls import path
from .import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.index, name="admin-dashboard"),
    path('register/', views.register,name="register-user"),
    path('login-user/', auth_view.LoginView.as_view(template_name= 'user/login.html'),
     name="login-user"),
    path('logout-user/', auth_view.LogoutView.as_view(template_name= 'user/logout.html'),
    name="logout-user"),
    path('password_reset/', auth_view.PasswordResetView.as_view(),
    name='password_reset'),
    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(),
    name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(),
    name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(),
    name='password_reset_complete'),
    path('student-registration/', views.registerStudent , name="student-registration"),
    path('record-sector/', views.record_sectors, name="record-sector"),
    path('sector-list/', views.displaySectors, name="sector-list"),
    path('student-list/', views.studentList, name="student-list"),
    path('reason-list/', views.displayReason, name="reason-list"),
    path('messageboard/', views.notifications, name="messageboard"),
    path('sectors/', views.sectors, name="sectors"),
    path('delete-student/<int:pk>/', views.deleteStudent, name="delete-student"),
    path('user-profile/', views.userProfile, name="user-profile"),
    path('edit-student/<int:pk>/', views.editStudent, name="edit-student"),
    path('gender/', views.countBygender, name="gender"),
    path('report/', views.createReport, name="report"),
    path('countbysector/', views.countBysector, name="countbysector"),
    path('sendmessage/', views.sendmessage, name="sendmessage"),
    path('report2/', views.generatereport2, name="report2"),
]
