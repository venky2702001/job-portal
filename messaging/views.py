from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from notifications.models import Notification
from .models import Message
from .forms import MessageForm
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# Create your views here.
# messaging/views.py

@login_required
def inbox(request):
    inbox_messages = Message.objects.filter(recipient=request.user)
    return render(request, "messaging/inbox.html", {"inbox_messages": inbox_messages})

@login_required
def sent_messages(request):
    sent_message_list = Message.objects.filter(sender=request.user)
    return render(request, "messaging/sent.html", {"sent_message_list": sent_message_list})

@login_required
def send_message(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            # 🔔 Create notification
            Notification.objects.create(
                recipient=msg.recipient,
                message=f"New message from {msg.sender.username}: {msg.subject}",
                url=f"/messaging/{msg.id}/"
            )

            # 🔔 Push notification to WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{msg.recipient.id}",
                {
                    "type": "notify",
                    "message": f"New message from {msg.sender.username}: {msg.subject}",
                    "url": f"/messaging/{msg.id}/"
                }
            )
            return redirect("messaging:inbox")
    else:
        form = MessageForm()
    return render(request, "messaging/send_message.html", {"form": form})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.is_read = True
    message.save()
    return render(request, "messaging/message_detail.html", {"message": message})
