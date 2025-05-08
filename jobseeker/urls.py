# jobseeker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.jobseeker_login, name='jobseeker_login'),
    path('register/', views.jobseeker_register, name='jobseeker_register'),
    path('dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('logout/', views.jobseeker_logout, name='jobseeker_logout'),
]
