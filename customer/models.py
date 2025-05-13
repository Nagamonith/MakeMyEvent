from django.db import models


class Customer(models.Model):
    from django.contrib.auth.models import User
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    # Optional extra fields:
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username if self.user else "No User Linked"
