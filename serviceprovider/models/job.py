from django.db import models
from .retailer import Retailer

class Job(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_entries = models.IntegerField(default=1)
    posted_on = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100, default='Not Specified')

    def __str__(self):
        return self.job_title
