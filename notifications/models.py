from django.db import models
from accounts.models import User

# Create your models here.


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="system_notifications")
    message = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)  # link to detail page
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"
