from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q
from messaging.models import Message
from accounts.utils import candidate_required, recruiter_required
from notifications.models import Notification
from .models import Job
from .forms import JobForm
from applications.models import Application
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@login_required

def job_list(request):
    if request.user.role == 'recruiter':
        return redirect('jobs:recruiter_dashboard')
    if request.user.role == 'admin':
        return redirect('admin:index')
    query = request.GET.get('q')
    location = request.GET.get('location')
    company = request.GET.get('company')
    sort = request.GET.get('sort', 'date')  # default sort by date

    jobs = Job.objects.all()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    if location:
        jobs = jobs.filter(location__icontains=location)
    if company:
        jobs = jobs.filter(company__icontains=company)

    # Sorting
    if sort == 'date':
        jobs = jobs.order_by('-created_at')  # newest first
    elif sort == 'company':
        jobs = jobs.order_by('company')
    elif sort == 'title':
        jobs = jobs.order_by('title')

    # Pagination
    paginator = Paginator(jobs, 5)  # 5 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'jobs/job_list.html', {'page_obj': page_obj})

@login_required
@recruiter_required
def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()

            # Send job alert
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "job_alerts",
                {
                    "type": "job_alert",
                    "title": job.title,
                    "company": job.company,
                    "location": job.location,
                }
            )
            return redirect('jobs:job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})

@login_required
@recruiter_required
def recruiter_dashboard(request):
    # Jobs posted by this recruiter
    jobs = Job.objects.filter(recruiter=request.user)

    # Applications received for those jobs
    applications = Application.objects.filter(job__in=jobs).select_related("candidate", "job")

    # Analytics counts
    jobs_posted_count = jobs.count()
    active_candidates_count = applications.values("candidate").distinct().count()
    hires_count = applications.filter(status="hired").count()

    # Unread messages
    unread_messages = Message.objects.filter(recipient=request.user, is_read=False).count()

    # Recent notifications
    notifications = Notification.objects.filter(recipient=request.user).order_by("-created_at")[:5]

    context = {
        "jobs": jobs,
        "applications": applications,
        "jobs_posted_count": jobs_posted_count,
        "active_candidates_count": active_candidates_count,
        "hires_count": hires_count,
        "unread_messages": unread_messages,
        "notifications": notifications,
    }
    return render(request, "jobs/recruiter_dashboard.html", context)


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
@recruiter_required
def job_edit(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('jobs:recruiter_dashboard')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form, 'edit_mode': True})

@login_required
@recruiter_required
def job_delete(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)

    if request.method == 'POST':
        job.delete()
        return redirect('jobs:recruiter_dashboard')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})
