from django.core.mail import send_mail
from django.conf import settings
from .models import Job
def send_notification_email(subject, message, recipient_list):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )


def recommend_jobs_for_candidate(candidate_profile):
    candidate_skills = candidate_profile.skills.split(",") if candidate_profile.skills else []
    candidate_skills = [skill.strip().lower() for skill in candidate_skills]

    recommended_jobs = Job.objects.none()

    for skill in candidate_skills:
        matches = Job.objects.filter(skills_required__icontains=skill)
        recommended_jobs = recommended_jobs | matches

    return recommended_jobs.distinct()


