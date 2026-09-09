from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import *
import logging 

User = get_user_model()
logger = logging.getLogger("recruiter_approvals")

# Bulk action: approve recruiters + send email
def approve_recruiters(modeladmin, request, queryset):
    for user in queryset.filter(role="recruiter", is_active=False):
        user.is_active = True
        user.save()

        # ✅ Save approval in DB
        RecruiterApprovalLog.objects.create(
            recruiter=user,
            approved_by=request.user,
            action="approved"
        )

        # ✅ Write approval to file log
        logger.info(f"Recruiter {user.username} approved by {request.user.username}")

        # Send approval email
        subject = "Your Recruiter Account Has Been Approved"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [user.email]

        html_content = render_to_string("emails/recruiter_approved.html", {
            "username": user.username,
            "portal_url": "http://127.0.0.1:8000/accounts/login/",
        })
        text_content = f"Hello {user.username},\n\nYour recruiter account has been approved. You can now log in.\n\nBest regards,\nJobPortal Team"

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

approve_recruiters.short_description = "Approve selected recruiters"

class RecruiterApprovalLogInline(admin.TabularInline):
    model = RecruiterApprovalLog
    fk_name = "recruiter"
    extra = 0
    readonly_fields = ("approved_by", "action", "timestamp")
    can_delete = False
    verbose_name_plural = "Approval History"
    classes = ("collapse",)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("username", "email")
    actions = [approve_recruiters]

    fieldsets = UserAdmin.fieldsets + (
        ("Role and Status", {"fields": ("role",)}),
    )
    inlines = [RecruiterApprovalLogInline]

@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "resume", "skills", "bio")

@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "website")

@admin.register(RecruiterApprovalLog)
class RecruiterApprovalLogAdmin(admin.ModelAdmin):
    list_display = ("recruiter", "approved_by", "action", "timestamp")
    list_filter = ("action", "approved_by", "timestamp")
    search_fields = ("recruiter__username", "approved_by__username")
    ordering = ("-timestamp",)

