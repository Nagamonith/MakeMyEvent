from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Customer
from django.contrib.auth.hashers import check_password, make_password
from serviceprovider.models import Service  # ✅ import your service model
from .models import Customer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

        # Link to Customer model
        Customer.objects.create(user=user)

        return redirect('customer_login')

    return render(request, 'customer_register.html')


# Customer Login
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Customer
from django.views.decorators.csrf import csrf_exempt

def customer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('customer_dashboard')  # Or another success URL
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'customer_login.html')


from .models import Customer
from serviceprovider.models import Service


from chat.models import ChatMessage  # 👈 Make sure to import this
from chat.models import ChatMessage

@login_required(login_url='customer_login')
def customer_dashboard(request):
    customer = Customer.objects.get(user=request.user)
    services = Service.objects.filter(available=True)
    received_messages = ChatMessage.objects.filter(receiver=request.user).order_by('-timestamp')  # 👈

    return render(request, 'customer/dashboard.html', {
        'customer': customer,
        'services': services,
        'received_messages': received_messages  # 👈
    })




from django.shortcuts import redirect
from django.contrib.auth import logout

def customer_logout(request):
    logout(request)  # Log out the current user
    return redirect('customer_login')  # Redirect to the login page after logging out


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from chat.models import ChatMessage
from serviceprovider.models import Retailer
from .models import Customer

@login_required(login_url='customer_login')
def send_message_to_retailer(request, retailer_id):
    # Check if it's a POST request
    if request.method == 'POST':
        message_text = request.POST.get('message')  # Get the message content
        
        # Fetch the retailer object
        retailer = get_object_or_404(Retailer, id=retailer_id)
        
        # Fetch the logged-in customer
        customer = Customer.objects.get(user=request.user)

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
  # or redirect to a chat page
from django.shortcuts import render
from django.http import HttpResponse

def chat_view(request, retailer_id):
    # Your logic for the chat view
    return HttpResponse(f"Chat with retailer {retailer_id}")
