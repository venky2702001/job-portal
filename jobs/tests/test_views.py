from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from jobs.models import Job
from applications.models import Application
from messaging.models import Message
from notifications.models import Notification

# Create your tests here.
class RecruiterDashboardViewTest(TestCase):
    def setUp(self):
        # Create recruiter user
        self.recruiter = User.objects.create_user(username="recruiter", password="pass123")
        self.client.login(username="recruiter", password="pass123")

        # Create candidate user
        self.candidate = User.objects.create_user(username="candidate", password="pass123")

        # Create job posted by recruiter
        self.job = Job.objects.create(title="Backend Developer", company="TechCorp", posted_by=self.recruiter)

        # Create application
        self.application = Application.objects.create(
            job=self.job,
            candidate=self.candidate,
            status="APPLIED"
        )

        # Create unread message
        self.message = Message.objects.create(
            sender=self.candidate,
            recipient=self.recruiter,
            subject="Hello",
            body="Interested in the role",
            is_read=False
        )

        # Create notification
        self.notification = Notification.objects.create(
            user=self.recruiter,
            message="New candidate applied"
        )

    def test_dashboard_context(self):
        response = self.client.get(reverse("recruiter_dashboard"))
        self.assertEqual(response.status_code, 200)

        # Check jobs
        self.assertIn(self.job, response.context["jobs"])

        # Check applications
        self.assertIn(self.application, response.context["applications"])

        # Check counts
        self.assertEqual(response.context["jobs_posted_count"], 1)
        self.assertEqual(response.context["active_candidates_count"], 1)
        self.assertEqual(response.context["hires_count"], 0)

        # Check unread messages
        self.assertEqual(response.context["unread_messages"], 1)

        # Check notifications
        self.assertIn(self.notification, response.context["notifications"])
