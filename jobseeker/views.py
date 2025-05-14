from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from serviceprovider.models import Job
from .models import JobSeeker, JobApplication
from django.core.mail import send_mail
from django.conf import settings

def jobseeker_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('jobseeker_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('jobseeker_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('jobseeker_register')

        # Create User and JobSeeker profile
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            JobSeeker.objects.create(user=user)
            
            # Log the user in directly after registration
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registration and login successful!')
                return redirect('jobseeker_dashboard')
                
        except Exception as e:
            messages.error(request, f'Error during registration: {str(e)}')
            return redirect('jobseeker_register')

    return render(request, 'jobseeker_register.html')

def jobseeker_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                # Check if user has a jobseeker profile
                jobseeker = user.jobseeker
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('jobseeker_dashboard')
            except JobSeeker.DoesNotExist:
                messages.error(request, "No jobseeker profile found. Please register.")
                return redirect('jobseeker_register')
        else:
            messages.error(request, 'Invalid username or password')
            # Add debug output
            print(f"Failed login attempt for username: {username}")
            if not User.objects.filter(username=username).exists():
                print("Username doesn't exist")
            else:
                print("Username exists but password is incorrect")
            return redirect('jobseeker_login')
    
    return render(request, 'jobseeker_login.html')

@login_required
def jobseeker_dashboard(request):
    try:
        jobseeker = request.user.jobseeker
    except JobSeeker.DoesNotExist:
        messages.error(request, "Please complete your jobseeker profile")
        return redirect('jobseeker_profile')  # You'll need to create this view

    jobs = Job.objects.all().order_by('-posted_on')
    
    # Get applications made by this jobseeker
    applications = JobApplication.objects.filter(jobseeker=request.user).select_related('job')
    
    return render(request, 'jobseeker_dashboard.html', {
        'jobseeker': jobseeker,
        'jobs': jobs,
        'applications': applications
    })

@login_required
def apply_for_job(request, job_id):
    try:
        jobseeker = request.user.jobseeker
    except JobSeeker.DoesNotExist:
        messages.error(request, "Please complete your jobseeker profile")
        return redirect('jobseeker_profile')
    
    job = Job.objects.get(id=job_id)
    
    # Check if already applied
    if JobApplication.objects.filter(job=job, jobseeker=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobseeker_dashboard')
    
    # Check available openings
    accepted_count = JobApplication.objects.filter(job=job, status='ACCEPTED').count()
    if accepted_count >= job.number_of_entries:
        messages.warning(request, 'No available openings for this job.')
        return redirect('jobseeker_dashboard')
    
    # Create application
    JobApplication.objects.create(
        job=job,
        jobseeker=request.user,
        status='PENDING'
    )
    
    messages.success(request, 'Your application has been submitted successfully!')
    return redirect('jobseeker_dashboard')

def jobseeker_logout(request):
    logout(request)
    return redirect('jobseeker_login')
@login_required
def jobseeker_profile(request):
    try:
        jobseeker = request.user.jobseeker
    except JobSeeker.DoesNotExist:
        jobseeker = JobSeeker(user=request.user)

    if request.method == 'POST':
        jobseeker.phone = request.POST.get('phone', '')
        # Add any additional fields from your JobSeeker model
        jobseeker.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('jobseeker_dashboard')

    return render(request, 'jobseeker/profile.html', {'jobseeker': jobseeker})