from django.contrib import admin
from serviceprovider.models import *


@admin.register(Retailer)
class RetailerAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_email')  # Display user fields in the list
    search_fields = ('user__username', 'user__email')  # Allow search by username and email

    def user_username(self, obj):
        return obj.user.username if obj.user else 'No User'  # Check if user exists
    user_username.admin_order_field = 'user__username'  # Sorting by username
    user_username.short_description = 'Username'  # Custom column name in the admin

    def user_email(self, obj):
        return obj.user.email if obj.user else 'No Email'  # Check if user exists
    user_email.admin_order_field = 'user__email'  # Sorting by email
    user_email.short_description = 'Email'  # Custom column name in the admin
admin.site.register(Job)
admin.site.register(Service)