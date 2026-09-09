from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from notifications.models import Notification
from .utils import send_notification_email
from .models import *
from .forms import ApplicationForm
from django.conf import settings
from jobs.models import Job
from interviews.models import Interview
from .utils import recommend_jobs_for_candidate
from accounts.utils import recruiter_required,candidate_required
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from messaging.models import Message



@login_required
@candidate_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    already_applied = Application.objects.filter(candidate=request.user, job=job).exists()
    if already_applied and request.method != 'POST':
        messages.info(request, "You've already applied to this job.")
        return redirect('applications:candidate_dashboard')

    if request.method == 'POST':
        if already_applied:
            messages.info(request, "You've already applied to this job.")
            return redirect('applications:candidate_dashboard')
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.candidate = request.user
            application.job = job
            application.save()

            # Candidate confirmation email
            subject = f"Application Submitted for {job.title}"
            message = (
                f"Dear {request.user.username},\n\n"
                f"You have successfully applied for '{job.title}' at {job.company}.\n\n"
                f"Best of luck!\nJob Portal Team"
            )
            send_notification_email(subject, message, [request.user.email])

            # Recruiter notification email
            subject = f"New Application for {job.title}"
            message = (
                f"Dear {job.recruiter.username},\n\n"
                f"Candidate {request.user.username} has applied for your job posting '{job.title}'.\n\n"
                f"Best regards,\nJob Portal Team"
            )
            send_notification_email(subject, message, [job.recruiter.email])

            return redirect('applications:candidate_dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'applications/apply_form.html', {'form': form, 'job': job})

@login_required
@candidate_required
def candidate_dashboard(request):
    applications = Application.objects.filter(candidate=request.user)

    # Candidate Profile
    profile = getattr(request.user, 'candidate_profile', None)

    # Recommend jobs based on skills
    recommended_jobs = []
    if profile and profile.skills:
        recommended_jobs = recommend_jobs_for_candidate(profile)

    saved_jobs = SavedJob.objects.filter(candidate=request.user)

    # Unread message count
    unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()

    # Profile completion
    completion = profile.profile_completion() if profile else 0

    # Recent notifications
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:5]

    # Upcoming interviews
    upcoming_interviews = Interview.objects.filter(
        candidate=request.user, scheduled_at__gte=timezone.now()
    ).order_by('scheduled_at')[:5]

    return render(request, 'applications/candidate_dashboard.html', {
        'applications': applications,
        'recommended_jobs': recommended_jobs,
        'saved_jobs': saved_jobs,
        'unread_count': unread_count,
        'completion': completion,
        'notifications': notifications,
        'upcoming_interviews': upcoming_interviews,
    })


@login_required
@recruiter_required
def update_status(request, app_id):

    # Ensure recruiter can only update applications for their own jobs
    application = get_object_or_404(Application, id=app_id, job__recruiter=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES).keys():
            application.status = new_status
            application.save()

            # 1️⃣ Create DB notification
            Notification.objects.create(
                recipient=application.candidate,
                message=f"Your application for {application.job.title} is now {application.get_status_display()}."
            )

            # 2️⃣ Send real-time notification via WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{application.candidate.id}",
                {
                    "type": "send_notification",
                    "message": f"Your application for {application.job.title} is now {application.get_status_display()}."
                }
            )

            # 3️⃣ Send email notification
            subject = f"Application Update for {application.job.title}"
            message = (
                f"Hello {application.candidate.username},\n\n"
                f"Your application for '{application.job.title}' has been updated.\n"
                f"New Status: {application.get_status_display()}\n\n"
                f"Best regards,\nJobPortal Team"
            )
            recipient = [application.candidate.email]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient)

        return redirect('jobs:recruiter_dashboard')

    return render(request, 'applications/update_status.html', {'application': application})

@login_required
@candidate_required
def application_history(request):
    applications = Application.objects.filter(candidate=request.user).select_related('job')
    return render(request, 'applications/application_history.html', {'applications': applications})

@login_required
@recruiter_required
def recruiter_analytics(request):

    jobs = Job.objects.filter(recruiter=request.user)
    applications = Application.objects.filter(job__in=jobs)

    # Count applications by status
    status_counts = applications.values('status').annotate(total=Count('id'))

    # Count applications per job
    job_counts = applications.values('job__title').annotate(total=Count('id'))

    return render(request, 'applications/recruiter_analytics.html', {
        'jobs': jobs,
        'status_counts': status_counts,
        'job_counts': job_counts,
    })


@login_required
@recruiter_required
def recruiter_applications(request):
    status = request.GET.get("status")
    job_id = request.GET.get("job")
    applications = Application.objects.filter(job__recruiter=request.user)

    if status:
        applications = applications.filter(status=status)
    if job_id:
        applications = applications.filter(job_id=job_id)

    return render(request, "applications/recruiter_applications.html", {
        "applications": applications,
        "jobs": Job.objects.filter(recruiter=request.user)
    })

#save/remove jobs
@login_required
@candidate_required
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    SavedJob.objects.get_or_create(candidate=request.user, job=job)
    return redirect('jobs:job_list')

@login_required
@candidate_required
def remove_saved_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    SavedJob.objects.filter(candidate=request.user, job=job).delete()
    return redirect('applications:saved_jobs')

@login_required
@candidate_required
def saved_jobs(request):
    jobs = SavedJob.objects.filter(candidate=request.user)
    return render(request, 'applications/saved_jobs.html', {'saved_jobs': jobs})