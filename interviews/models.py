from django.db import models
from accounts.models import User
from jobs.models import Job


# Create your models here.
# interviews/models.py

class Interview(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scheduled_interviews")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interviews")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("declined", "Declined"), ("reschedule", "Reschedule")],
        default="pending"
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Interview for {self.job.title} with {self.candidate.username}"
