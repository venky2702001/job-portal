from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.utils import *
from .models import Interview
from .forms import InterviewForm
from notifications.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your views here.
# interviews/views.py

@login_required
@recruiter_required
def schedule_interview(request):
    if request.user.role != "recruiter":
        return render(request, "403.html", status=403)
     # Check if recruiter is rescheduling an existing interview
    reschedule_id = request.GET.get("reschedule")
    interview_instance = None
    if reschedule_id:
        interview_instance = get_object_or_404(Interview, id=reschedule_id, recruiter=request.user)

    initial = {}
    if not interview_instance:
        if request.GET.get("candidate"):
            initial["candidate"] = request.GET.get("candidate")
        if request.GET.get("job"):
            initial["job"] = request.GET.get("job")

    if request.method == "POST":
        form = InterviewForm(request.POST, instance=interview_instance, recruiter=request.user)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.recruiter = request.user
            interview.save()

            # 🔔 Create notification in DB
            Notification.objects.create(
                recipient=interview.candidate,
                message=f"Interview scheduled for {interview.job.title} on {interview.scheduled_at}",
                url=f"/interviews/candidate/"
            )

            # 🔔 Push notification to WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{interview.candidate.id}",
                {
                    "type": "notify",
                    "message": f"Interview scheduled for {interview.job.title} on {interview.scheduled_at}",
                    "url": f"/interviews/candidate/"
                }
            )
            return redirect("interviews:recruiter_interviews")
    else:
        form = InterviewForm(instance=interview_instance, recruiter=request.user, initial=initial)
    return render(request, "interviews/schedule_interview.html", {"form": form})

@login_required
@candidate_required
def candidate_interviews(request):
    interviews = Interview.objects.filter(candidate=request.user)
    return render(request, "interviews/candidate_interviews.html", {"interviews": interviews})

@login_required
def update_interview_status(request, interview_id, status):
    interview = get_object_or_404(Interview, id=interview_id)

    valid_statuses = ["confirmed", "declined", "pending", "reschedule"]
    if status not in valid_statuses:
        return render(request, "403.html", status=403)

    if request.user.role == "candidate":
        if interview.candidate != request.user:
            return render(request, "403.html", status=403)
        interview.status = status
        interview.save()
        return redirect("interviews:candidate_interviews")

    elif request.user.role == "recruiter":
        if interview.recruiter != request.user:
            return render(request, "403.html", status=403)
        interview.status = status
        interview.save()
        return redirect("interviews:recruiter_interviews")

    return render(request, "403.html", status=403)


@login_required
@recruiter_required
def recruiter_interviews(request):
    interviews = Interview.objects.filter(recruiter=request.user)
    return render(request, "interviews/recruiter_interviews.html", {"interviews": interviews})
