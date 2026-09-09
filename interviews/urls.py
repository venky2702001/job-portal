from django.urls import path
from . import views

app_name = "interviews"

urlpatterns = [
    path("schedule/", views.schedule_interview, name="schedule_interview"),
    path("candidate/", views.candidate_interviews, name="candidate_interviews"),
    path("<int:interview_id>/<str:status>/", views.update_interview_status, name="update_interview_status"),
    path("recruiter/", views.recruiter_interviews, name="recruiter_interviews"),
    
]
