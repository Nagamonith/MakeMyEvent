from django.db import models
from django.contrib.auth.models import User
from serviceprovider.models import Job

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    # Add any other profile fields you need
    
    def __str__(self):
        return self.user.username

class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    jobseeker = models.ForeignKey(User, on_delete=models.CASCADE)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected')
    ], default='PENDING')
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.jobseeker.username} - {self.job.job_title} ({self.status})"