from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import StyledPasswordResetForm, StyledSetPasswordForm

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

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='emails/password_reset_email.html',
        subject_template_name='emails/password_reset_subject.txt',
        form_class=StyledPasswordResetForm,
        success_url='/accounts/password-reset/done/',
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        form_class=StyledSetPasswordForm,
        success_url='/accounts/reset/done/',
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html',
    ), name='password_reset_complete'),
]