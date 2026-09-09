# interviews/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from jobs.models import Job
from interviews.models import Interview

User = get_user_model()

class InterviewViewTest(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(username="recruiter", password="pass123", role="recruiter")
        self.candidate = User.objects.create_user(username="candidate", password="pass123", role="candidate")
        self.job = Job.objects.create(title="Backend Developer", company="TechCorp", location="Remote", recruiter=self.recruiter)

    def test_schedule_interview(self):
        self.client.login(username="recruiter", password="pass123")
        response = self.client.post(reverse("interviews:schedule_interview"), {
            "candidate": self.candidate.id,
            "job": self.job.id,
            "scheduled_at": "2026-08-30 10:00:00",
            "location": "Zoom"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Interview.objects.count(), 1)

    def test_candidate_view_interviews(self):
        Interview.objects.create(job=self.job, candidate=self.candidate, recruiter=self.recruiter,
                                 scheduled_at="2026-08-30 10:00:00", location="Zoom")
        self.client.login(username="candidate", password="pass123")
        response = self.client.get(reverse("interviews:candidate_interviews"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Backend Developer")
