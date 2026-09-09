from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('update/<int:app_id>/',views.update_status,name='update_status'),
    path('history/', views.application_history, name='application_history'),
    path('analytics/', views.recruiter_analytics, name='recruiter_analytics'),
    path('recruiter/applications/', views.recruiter_applications, name='recruiter_applications'),
    path('save/<int:job_id>/', views.save_job, name='save_job'),
    path('unsave/<int:job_id>/', views.remove_saved_job, name='remove_saved_job'),
    path('saved/', views.saved_jobs, name='saved_jobs'),
]
