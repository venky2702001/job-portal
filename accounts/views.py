from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseForbidden
from applications.models import Application
from jobportal import settings
from jobs.models import Job
from .forms import CandidateProfileForm, CustomUserCreationForm, RecruiterProfileForm, RecruiterSignupForm, StyledAuthenticationForm
from .models import CandidateProfile, RecruiterProfile
from .utils import *
from django.db.models import Q


# --- Existing Auth Views ---
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('jobs:job_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = StyledAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # ✅ Redirect based on role
            if user.role == "candidate":
                return redirect("applications:candidate_dashboard")
            elif user.role == "recruiter":
                return redirect("jobs:recruiter_dashboard")
            else:
                return redirect("jobs:job_list")  # fallback
    else:
        form = StyledAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})
@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

def recruiter_signup_view(request):
    if request.method == 'POST':
        form = RecruiterSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Notify admin by email
            send_mail(
                subject="New Recruiter Signup Pending Approval",
                message=f"A new recruiter '{user.username}' from company '{form.cleaned_data['company']}' has registered and needs approval.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],  # define in settings.py
            )
            return render(request, 'accounts/pending_approval.html')
    else:
        form = RecruiterSignupForm()
    return render(request, 'accounts/recruiter_signup.html', {'form': form})

# --- New Profile Views ---
#candidate profile edit view
@login_required
@candidate_required
def edit_candidate_profile(request):
    profile, created = CandidateProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CandidateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Only auto-fill skills from a newly uploaded resume if the
            # candidate didn't type their own skills in this submission
            if 'resume' in request.FILES and not form.cleaned_data.get('skills'):
                text = extract_text_from_resume(profile.resume)
                skills = extract_skills(text)
                if skills:
                    profile.skills = skills
                    profile.save()
            return redirect('applications:candidate_dashboard')
    else:
        form = CandidateProfileForm(instance=profile)
    return render(request, 'accounts/edit_candidate_profile.html', {'form': form})


#candidate search view for recruiters
@login_required
@recruiter_required
def candidate_search(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    status = request.GET.get('status', '')

    candidates = CandidateProfile.objects.all()

    if query:
        candidates = candidates.filter(
            Q(skills__icontains=query) | Q(bio__icontains=query)
        )
    if location:
        candidates = candidates.filter(location__icontains=location)
    if status:
        candidates = candidates.filter(user__applications__status=status).distinct()

    return render(request, 'accounts/candidate_search.html', {
        'candidates': candidates,
        'query': query,
        'location': location,
        'status': status,
    })


#recruiter profile edit view
@login_required
@recruiter_required
def edit_recruiter_profile(request):
    profile, created = RecruiterProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = RecruiterProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('jobs:recruiter_dashboard')
    else:
        form = RecruiterProfileForm(instance=profile)
    return render(request, 'accounts/edit_recruiter_profile.html', {'form': form})

#admin analytics view
@login_required
@admin_required
def admin_analytics(request):
    jobs_count = Job.objects.count()
    applications_count = Application.objects.count()
    candidates_count = CandidateProfile.objects.count()

    return render(request, 'accounts/admin_analytics.html', {
        'jobs_count': jobs_count,
        'applications_count': applications_count,
        'candidates_count': candidates_count,
    })



@login_required
def download_resume(request, candidate_id):
    candidate = get_object_or_404(CandidateProfile, id=candidate_id)
    # Only the candidate themselves, or a recruiter who received an
    # application from this candidate for one of their own jobs, can download
    is_owner = request.user == candidate.user
    is_relevant_recruiter = (
        request.user.role == 'recruiter'
        and Application.objects.filter(
            candidate=candidate.user, job__recruiter=request.user
        ).exists()
    )
    if is_owner or is_relevant_recruiter:
        if not candidate.resume:
            return HttpResponseForbidden("No resume uploaded.")
        return FileResponse(candidate.resume.open(), as_attachment=True)
    return HttpResponseForbidden("You do not have permission to access this resume.")
