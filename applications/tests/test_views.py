from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from applications.models import Application, SavedJob
from jobs.models import Job
from messaging.models import Message
from notifications.models import Notification
from accounts.models import CandidateProfile
User = get_user_model()
class CandidateDashboardViewTest(TestCase):
    def setUp(self):
        # Create candidate user
        self.candidate = User.objects.create_user(username="candidate", password="pass123")
        self.client.login(username="candidate", password="pass123")

        # Candidate profile
        self.profile = CandidateProfile.objects.create(
            user=self.candidate,
            skills="Python, Django",
            location="Remote",
            bio="Full-stack developer",
        )

        # Job
        self.recruiter = User.objects.create_user(username="recruiter", password="pass123", role="recruiter")
        self.job = Job.objects.create(
            title="Backend Developer",
            company="TechCorp",
            location="Remote",
            recruiter=self.recruiter   # must assign recruiter
        )


        # Application
        self.application = Application.objects.create(
            job=self.job,
            candidate=self.candidate,
            status="APPLIED"
        )

        # Saved job
        self.saved_job = SavedJob.objects.create(candidate=self.candidate, job=self.job)

        # Unread message
        self.message = Message.objects.create(
            sender=self.candidate,
            recipient=self.candidate,  # for simplicity
            subject="Test",
            body="Hello",
            is_read=False
        )

        # Notification
        self.notification = Notification.objects.create(
            recipient=self.candidate,
            message="Profile updated"
        )

    def test_dashboard_context(self):
        response = self.client.get(reverse("applications:candidate_dashboard"))
        self.assertEqual(response.status_code, 200)

        # Applications
        self.assertIn(self.application, response.context["applications"])

        # Recommended jobs (assuming recommend_jobs_for_candidate returns something)
        self.assertIn(self.job, response.context["recommended_jobs"])

        # Saved jobs
        self.assertIn(self.saved_job, response.context["saved_jobs"])

        # Unread count
        self.assertEqual(response.context["unread_count"], 1)

        # Profile completion
        self.assertGreaterEqual(response.context["completion"], 0)

        # Notifications
        self.assertIn(self.notification, response.context["notifications"])
