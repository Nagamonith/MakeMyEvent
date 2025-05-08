from django.db import models
from django.contrib.auth.models import User
from .retailer import Retailer
from customer.models import Customer  # Assuming Customer is in a separate app

class ChatMessage(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.customer.user.username}"
