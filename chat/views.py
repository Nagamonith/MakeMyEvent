from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound
# from .models import ChatMessage
# from serviceprovider.models import Retailer
# from customer.models import Customer

@login_required(login_url='customer_login')
def chat_view(request, retailer_id):
    from .models import ChatMessage  # Import moved inside the function
    from serviceprovider.models import Retailer
    from customer.models import Customer
    try:
        retailer = Retailer.objects.get(id=retailer_id)
    except Retailer.DoesNotExist:
        return HttpResponseNotFound("The requested retailer does not exist.")
    customer = get_object_or_404(Customer, user=request.user)

    # Generate a unique room name based on customer and retailer IDs
    room_name = f"room_{customer.id}_{retailer.id}"

    # Fetch the chat messages between this customer and retailer
    messages = ChatMessage.objects.filter(customer=customer, retailer=retailer).order_by('timestamp')

    return render(request, 'chat/chat_view.html', {
        'retailer': retailer,
        'customer': customer,
        'messages': messages,
        'room_name': room_name,  # Pass the room name to the template
    })