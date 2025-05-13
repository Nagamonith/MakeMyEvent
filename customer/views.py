from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Customer
from serviceprovider.models import Service, Retailer
from chat.models import ChatMessage  # Correct import
from django.db.models import Q
# Customer Registration
def customer_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Create User
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Hash the password
        )

        # Create Customer and link to User
        Customer.objects.create(user=user)

        return redirect('customer_login')

    return render(request, 'customer_register.html')

# Customer Login
def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('customer_dashboard')  # Redirect to customer dashboard
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'customer_login.html')

# Customer Dashboard


@login_required(login_url='customer_login')
def customer_dashboard(request):
    # Fetch the logged-in customer's data
    customer = get_object_or_404(Customer, user=request.user)

    # Fetch available services
    services = Service.objects.filter(available=True)

    # Fetch messages where the logged-in customer is either the sender or the receiver (customer)
    received_messages = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(customer=customer)
    ).order_by('-timestamp')

    return render(request, 'customer/dashboard.html', {
        'customer': customer,
        'services': services,
        'received_messages': received_messages
    })


# Customer Logout
def customer_logout(request):
    logout(request)  # Log out the current user
    return redirect('customer_login')  # Redirect to the login page after logging out

# Send message to retailer (this is the functionality for customers to send messages)
@login_required(login_url='customer_login')
def send_message_to_retailer(request, retailer_id):
    # Check if it's a POST request
    if request.method == 'POST':
        message_text = request.POST.get('message')  # Get the message content
        
        # Fetch the retailer object
        retailer = get_object_or_404(Retailer, id=retailer_id)
        
        # Fetch the logged-in customer
        customer = get_object_or_404(Customer, user=request.user)

        # Create and save the message to the database
        message = ChatMessage.objects.create(
            sender=request.user,        # logged-in customer (User)
            retailer=retailer,           # The retailer the customer is messaging
            customer=customer,          # The customer sending the message
            message=message_text        # The content of the message
        )
        
        # Optionally, redirect to a chat page where the conversation can continue
        return redirect('chat_view', retailer_id=retailer.id)

    # If it's not a POST request, redirect back to the customer dashboard
    return redirect('customer_dashboard')

# Chat view to display messages between customer and retailer
@login_required(login_url='customer_login')
def chat_view(request, retailer_id):
    # Fetch the retailer and customer objects
    retailer = get_object_or_404(Retailer, id=retailer_id)
    customer = get_object_or_404(Customer, user=request.user)

    # Fetch the chat messages between this customer and retailer
    messages = ChatMessage.objects.filter(customer=customer, retailer=retailer).order_by('timestamp')

    return render(request, 'chat/chat_view.html', {
        'retailer': retailer,
        'customer': customer,
        'messages': messages,
    })
