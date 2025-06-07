from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.serviceprovider_login, name='serviceprovider_login'),
    path('register/', views.serviceprovider_register, name='serviceprovider_register'),
    path('dashboard/', views.retailer_dashboard, name='retailer_dashboard'),
    path('add-service/', views.service_entry, name='addservice'),
    path('postjob/', views.postjob, name='postjob'),  # One clear path for posting jobs
    path('service-entry/', views.service_entry, name='service_entry'),
    # path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('myservices/', views.my_services, name='my_services'),
    path('editservice/<int:service_id>/', views.edit_service, name='edit_service'),
    path('create-retailer/', views.create_retailer, name='create_retailer'),  # Fixed path
    path('retailer-registration/', views.serviceprovider_register, name='retailer-registration'),  # Registration page
    path('application/<int:application_id>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('application/update/<int:application_id>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('payment_dashboard/', views.payment_dashboard, name='payment_dashboard'),
    path('process_payment/<int:payment_id>/', views.process_payment, name='process_payment'),
    path('razorpay-callback/', views.razorpay_callback, name='razorpay_callback'),
]
