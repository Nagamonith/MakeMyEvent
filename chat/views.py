from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import ChatMessage
from django.contrib.auth.models import User

@login_required
def chat_view(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    messages = ChatMessage.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by('timestamp')

    if request.method == "POST":
        msg = request.POST.get('message')
        if msg:
            ChatMessage.objects.create(sender=request.user, receiver=receiver, message=msg)
        return redirect('chat_view', receiver_id=receiver.id)

    return render(request, 'chat/chat.html', {'receiver': receiver, 'messages': messages})
