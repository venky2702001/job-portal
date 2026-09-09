from django.db import models
from accounts.models import User
from jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES=[
        ('applied','Applied'),
        ('reviewed','Reviewed'),
        ('accepted','Accepted'),
        ('rejected','Rejected'),
        ('hired','Hired'),
    ]
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title} ({self.status})"

class SavedJob(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'candidate'})
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f"{self.candidate.username} saved {self.job.title}"


