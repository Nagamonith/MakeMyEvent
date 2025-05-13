# serviceprovider/models.py
from django.db import models


class ChatMessage(models.Model):
    from django.contrib.auth.models import User
    retailer = models.ForeignKey('retailer.Retailer', on_delete=models.CASCADE)  # Lazy import for Retailer
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)  # Lazy import for Customer
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.customer.username}"
