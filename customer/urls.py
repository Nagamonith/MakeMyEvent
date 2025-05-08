# customer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.customer_login, name='customer_login'),
    path('register/', views.customer_register, name='customer_register'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
     path('chat/<int:retailer_id>/', views.chat_view, name='chat_view'),  # Example chat view URL
    path('send-message/<int:retailer_id>/', views.send_message_to_retailer, name='send_message_to_retailer'),
    path('logout/', views.customer_logout, name='customer_logout'),  # Logout URL
]
