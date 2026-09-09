from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('create/', views.job_create, name='job_create'),
    path('dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
    path('<int:job_id>/edit/', views.job_edit, name='job_edit'),
    path('<int:job_id>/delete/', views.job_delete, name='job_delete'),
    
]
