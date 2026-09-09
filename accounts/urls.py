from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('candidate/profile/',views.edit_candidate_profile,name='edit_candidate_profile'),
    path('recruiter/profile/',views.edit_recruiter_profile,name='edit_recruiter_profile'),
    path('candidate-search/', views.candidate_search, name='candidate_search'),
    path('admin-analytics/', views.admin_analytics, name='admin_analytics'),
    path('download-resume/<int:candidate_id>/', views.download_resume, name='download_resume'),
    path('recruiter-signup/', views.recruiter_signup_view, name='recruiter_signup'),
]
