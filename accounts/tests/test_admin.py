from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from accounts.admin import approve_recruiters
from accounts.models import RecruiterApprovalLog

User = get_user_model()

class MockRequest:
    def __init__(self, user):
        self.user = user

class ApproveRecruitersTest(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@test.com", password="pass"
        )
        self.recruiter = User.objects.create_user(
            username="recruiter1", email="rec@test.com", password="pass", role="recruiter", is_active=False
        )

    def test_bulk_approve_creates_log_and_activates_user(self):
        queryset = User.objects.filter(id=self.recruiter.id)
        approve_recruiters(None, MockRequest(self.admin_user), queryset)

        self.recruiter.refresh_from_db()
        self.assertTrue(self.recruiter.is_active)

        log = RecruiterApprovalLog.objects.get(recruiter=self.recruiter)
        self.assertEqual(log.approved_by, self.admin_user)
        self.assertEqual(log.action, "approved")
