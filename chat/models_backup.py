<<<<<<< HEAD
from django.db import models

from serviceprovider.models import Retailer
from customer.models import Customer
=======
from django.contrib.auth.models import User
from django.db import models
>>>>>>> e0fff1c11a062e64de0308567842cf4ae7737b6e

class ChatMessage(models.Model):
    from django.contrib.auth.models import User
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name='retailer_messages', default=1)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_messages', default=1)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
<<<<<<< HEAD
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'From {self.sender.username} to {self.retailer if self.sender == self.customer.user else self.customer}'

    class Meta:
        ordering = ['timestamp']
=======

    def __str__(self):
        return f'From {self.sender} to {self.receiver}'
>>>>>>> e0fff1c11a062e64de0308567842cf4ae7737b6e
