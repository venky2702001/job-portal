
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# Create your views here.
# messaging/views.py


@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user)
    return render(request, "notifications/list.html", {"notifications": notifications})

@login_required
def mark_as_read(request, notification_id):
    notif = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notif.is_read = True
    notif.save()
    return redirect(notif.url or "notifications:list")

@login_required
def mark_as_read_ajax(request, notification_id):
    notif = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notif.is_read = True
    notif.save()

    # Broadcast to WebSocket group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{request.user.id}",
        {
            "type": "read",
            "id": notif.id
        }
    )

    return JsonResponse({"success": True})


@login_required
def mark_all_as_read_ajax(request):
    # Mark all unread notifications for this user as read
    request.user.system_notifications.filter(is_read=False).update(is_read=True)

    # Broadcast to all tabs
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{request.user.id}",
        {
            "type": "read_all"
        }
    )

    return JsonResponse({"success": True})