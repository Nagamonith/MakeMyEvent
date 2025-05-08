from django.db import models
from .retailer import Retailer

class Service(models.Model):
    image_url = models.URLField(max_length=500)
    service_type = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=255)
    description = models.TextField()
    website_link = models.URLField(max_length=500)
    retailer = models.ForeignKey(Retailer, related_name="services", on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    def __str__(self):
        return f"Service: {self.service_type} by {self.company_name}"

