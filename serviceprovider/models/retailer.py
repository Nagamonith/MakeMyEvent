# serviceprovider/models/retailer.py
from django.db import models
from django.contrib.auth.models import User

class Retailer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="retailer", null=False, blank=False)
    #business_name = models.CharField(max_length=255,default='N/A')

    def __str__(self):
        return self.user.username
