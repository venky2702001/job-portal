from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class User(AbstractUser):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='candidate')
    created_at = models.DateTimeField(auto_now_add=True)

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    def profile_completion(self):
        fields = [self.skills, self.location, self.resume, self.bio]
        filled = sum(1 for f in fields if f)
        return int((filled / len(fields)) * 100)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=200)
    company_description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"


class RecruiterApprovalLog(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="approval_logs")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="approvals_given")
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)  # e.g. "approved", "rejected"

    def __str__(self):
        return f"{self.recruiter} {self.action} by {self.approved_by} at {self.timestamp}"
