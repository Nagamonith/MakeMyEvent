from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    # Use a string for the foreign key to avoid immediate import
    job_application = models.ForeignKey('jobseeker.JobApplication', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_to = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed')
    ], default='PENDING')
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.job_application.job.job_title} to {self.paid_to.username}"