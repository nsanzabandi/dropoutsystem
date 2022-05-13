
from os import name
from django.urls import path
from .import views
from .views import loginpage

urlpatterns = [
    path('index/', views.home, name="index"),
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutpage, name="logout"),
    path('index/', views.indexpage, name="index"),
    path('index2/', views.registerstudent, name="add_student"),
    path('ajax/load-sectors/', views.load_sectors, name="load_sectors"),
    path('index/', views.reasons, name="reasons"),
    
]
