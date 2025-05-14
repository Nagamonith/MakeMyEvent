from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User  # Add this import

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from .models import Retailer, ChatMessage
from django.db.models import Q
# serviceprovider/views.py
from serviceprovider.models import *
from customer.models import Customer




# Service Provider Registration
def serviceprovider_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if username or email already exists
        if Retailer.objects.filter(user__username=username).exists() or Retailer.objects.filter(user__email=email).exists():
            messages.error(request, "Username or email already exists.")
            return render(request, 'serviceprovider_register.html')

        # Create user first
        user = User.objects.create_user(username=username, email=email, password=password)
        retailer = Retailer(user=user)
        retailer.save()

        messages.success(request, "Registered successfully. Please log in.")
        return redirect('serviceprovider_login')

    return render(request, 'serviceprovider_register.html')

def serviceprovider_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            retailer = Retailer.objects.get(user=user)
            if retailer:
                login(request, user)
                request.session['retailer_id'] = retailer.id
                request.session['retailer_username'] = retailer.user.username
                
                # Redirect to the page the user was trying to access before login
                next_url = request.GET.get('next', 'retailer_dashboard')  # Default to dashboard
                return redirect(next_url)
            else:
                messages.error(request, "You are not registered as a retailer.")
                return redirect('serviceprovider_register')
        else:
            messages.error(request, "Invalid login credentials.")
            return redirect('serviceprovider_login')

    return render(request, 'serviceprovider_login.html')





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Retailer, ChatMessage
from customer.models import Customer
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Retailer, ChatMessage
from customer.models import Customer
from django.contrib.auth.models import User

from django.contrib import messages
from jobseeker.models import JobApplication
from django.core.mail import send_mail
from django.conf import settings
@login_required
def retailer_dashboard(request):
    try:
        retailer = Retailer.objects.get(user=request.user)
        print(f"Retailer found: {retailer.user.username}")
    except Retailer.DoesNotExist:
        messages.error(request, "You are not registered as a retailer.")
        return redirect('retailer-registration')

    # Get all jobs posted by this retailer
    jobs = Job.objects.filter(retailer=retailer)
    
    # Get all applications for these jobs
    applications = JobApplication.objects.filter(job__in=jobs).select_related('job', 'jobseeker')
    
    # Chat functionality (your existing code)
    customer_id = request.GET.get('customer_id')
    selected_customer = None
    messages_qs = []
    room_name = ""

    if customer_id:
        try:
            customer_user = User.objects.get(id=customer_id)
            selected_customer = Customer.objects.get(user=customer_user)
            
            user_ids = sorted([request.user.id, customer_user.id])
            room_name = f"{user_ids[0]}_{user_ids[1]}"

            messages_qs = ChatMessage.objects.filter(
                Q(sender=request.user, retailer=retailer, customer=selected_customer) |
                Q(sender=customer_user, retailer=retailer, customer=selected_customer)
            ).order_by('timestamp')

            if request.user != customer_user:
                unread_messages = messages_qs.filter(sender=customer_user, is_read=False)
                unread_messages.update(is_read=True)
                
        except (User.DoesNotExist, Customer.DoesNotExist):
            messages.error(request, "Selected customer not found.")

    customer_ids = ChatMessage.objects.filter(
        retailer=retailer
    ).values_list('customer', flat=True).distinct()
    customers = Customer.objects.filter(id__in=customer_ids)

    return render(request, 'retailer_dashboard.html', {
        'retailer': retailer,
        'jobs': jobs,
        'applications': applications,
        'messages': messages_qs,
        'customers': customers,
        'selected_customer': selected_customer,
        'room_name': room_name
    })
def update_application_status(request, application_id, status):
    if not request.user.is_authenticated:
        return redirect('serviceprovider_login')
    
    try:
        application = JobApplication.objects.get(id=application_id)
        if application.job.retailer.user != request.user:
            messages.error(request, "You don't have permission to update this application.")
            return redirect('retailer_dashboard')
        
        application.status = status
        application.save()
        
        if status == 'ACCEPTED':
            # Debugging: Print jobseeker details before sending email
            print("\n--- DEBUG: Email Recipient Check ---")
            print(f"Jobseeker Username: {application.jobseeker.username}")
            print(f"Jobseeker Email: {application.jobseeker.email}")
            print(f"Job Title: {application.job.job_title}")
            print(f"Retailer Email (Request User): {request.user.email}")  # Check if this matches where emails are going
            print("----------------------------------\n")

            # Send email to jobseeker
            subject = f"Your application for {application.job.job_title} has been accepted!"
            message = f"""
            Dear {application.jobseeker.username},
            
            We are pleased to inform you that your application for the position of 
            {application.job.job_title} has been accepted!
            
            Job Details:
            - Title: {application.job.job_title}
            - Description: {application.job.description}
            - Requirements: {application.job.requirements}
            - Payment: ₹{application.job.payment}
            - Location: {application.job.location}
            
            Please contact the service provider for further instructions.
            
            Best regards,
            {application.job.retailer.user.username}
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [application.jobseeker.email],  # Verify this is correct in the debug output
                fail_silently=False,
            )
            messages.success(request, "Application accepted and notification email sent!")
        else:
            messages.success(request, "Application status updated.")
            
    except JobApplication.DoesNotExist:
        messages.error(request, "Application not found.")
    
    return redirect('retailer_dashboard')







# views.py
def postjob(request):
    if 'retailer_id' not in request.session:
        return redirect('serviceprovider_login')

    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        payment = request.POST.get('payment')
        number_of_entries = request.POST.get('number_of_entries')
        location = request.POST['location'] 
        print("Form data:", job_title, description, requirements, payment, number_of_entries)  # Debug

        if not all([job_title, description, requirements, payment, number_of_entries]):
            messages.error(request, "All fields are required.")
            return redirect('postjob')

        try:
            retailer = Retailer.objects.get(id=request.session['retailer_id'])
        except Retailer.DoesNotExist:
            messages.error(request, "Retailer not found.")
            return redirect('serviceprovider_login')

        job = Job.objects.create(
            retailer=retailer,
            job_title=job_title,
            description=description,
            requirements=requirements,
            payment=payment,
            number_of_entries=number_of_entries
        )
        print("Job Created:", job)  # Debug confirmation

        messages.success(request, 'Job posted successfully!')
        return redirect('retailer_dashboard')

    return render(request, 'postjob.html')


# Create Retailer Profile
@login_required
def create_retailer(request):
    if request.method == 'POST':
        retailer = Retailer(user=request.user)
        retailer.save()
        messages.success(request, "Retailer profile created successfully.")
        return redirect('service_entry')  # After creating the retailer profile, redirect to service entry

    return render(request, 'create_retailer.html')  # Render a form to create retailer profile

# Service Provider Logout
def serviceprovider_logout(request):
    logout(request)
    return redirect('serviceprovider_login')
def my_services(request):
    if not request.user.is_authenticated:
        return redirect('login')

    retailer = Retailer.objects.get(user=request.user)
    services = Service.objects.filter(retailer=retailer)

    return render(request, 'my_service.html', {'services': services, 'retailer': retailer})
@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id, retailer__user=request.user)

    if request.method == 'POST':
        service.image_url = request.POST['image_url']
        service.service_type = request.POST['service_type']
        service.company_name = request.POST['company_name']
        service.specialization = request.POST['specialization']
        service.description = request.POST['description']
        service.website_link = request.POST['website_link']
        service.save()
        return redirect('my_services')

    return render(request, 'edit_service.html', {'service': service})
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service  # Adjust if your model is named differently

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Service, Retailer

def service_entry(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in as a retailer to add a service.")
        return redirect('login')  # or a specific login route

    try:
        retailer = Retailer.objects.get(user=request.user)
    except Retailer.DoesNotExist:
        messages.error(request, "Only registered retailers can add services.")
        return redirect('home')  # or show an error page

    if request.method == 'POST':
        image_url = request.POST.get('image_url')
        service_type = request.POST.get('service_type')
        company_name = request.POST.get('company_name')
        specialization = request.POST.get('specialization')
        description = request.POST.get('description')
        website_link = request.POST.get('website_link')

        if all([image_url, service_type, company_name, specialization, description, website_link]):
            Service.objects.create(
                image_url=image_url,
                service_type=service_type,
                company_name=company_name,
                specialization=specialization,
                description=description,
                website_link=website_link,
                retailer=retailer
            )
            messages.success(request, "Service added successfully!")
            return redirect('addservice')  # or a success page
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'service_entry.html')
