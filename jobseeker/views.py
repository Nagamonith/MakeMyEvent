from django.shortcuts import render, redirect
from django.contrib import messages
from .models import JobSeeker
from django.contrib.auth.hashers import make_password, check_password
from serviceprovider.models import *
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

        if JobSeeker.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('jobseeker_register')

        if JobSeeker.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('jobseeker_register')

        # Save to database
        hashed_password = make_password(password)
        jobseeker = JobSeeker(username=username, email=email, password=hashed_password)
        jobseeker.save()

        messages.success(request, 'Registration successful. Please login.')
        return redirect('jobseeker_login')

    return render(request, 'jobseeker_register.html')


def jobseeker_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            jobseeker = JobSeeker.objects.get(username=username)

            if check_password(password, jobseeker.password):
                request.session['jobseeker_id'] = jobseeker.id
                return redirect('jobseeker_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('jobseeker_login')

        except JobSeeker.DoesNotExist:
            messages.error(request, 'Invalid username or password')
            return redirect('jobseeker_login')

    return render(request, 'jobseeker_login.html')



def jobseeker_dashboard(request):
    jobseeker_id = request.session.get('jobseeker_id')
    if not jobseeker_id:
        return redirect('jobseeker_login')

    jobseeker = JobSeeker.objects.get(id=jobseeker_id)
    jobs = Job.objects.all().order_by('-posted_on')  # Fetch all job posts

    return render(request, 'jobseeker_dashboard.html', {
        'jobseeker': jobseeker,
        'jobs': jobs
    })


def jobseeker_logout(request):
    request.session.flush()
    return redirect('jobseeker_login')
