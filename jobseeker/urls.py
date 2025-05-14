# jobseeker/urls.py
from django.urls import path
from . import views

# jobseeker/urls.py
urlpatterns = [
    path('login/', views.jobseeker_login, name='jobseeker_login'),
    path('register/', views.jobseeker_register, name='jobseeker_register'),
    path('dashboard/', views.jobseeker_dashboard, name='jobseeker_dashboard'),
    path('apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('logout/', views.jobseeker_logout, name='jobseeker_logout'),
    path('profile/', views.jobseeker_profile, name='jobseeker_profile'),

]
