from django import forms
from .models import CandidateProfile, RecruiterProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import *
from jobportal.formutils import BootstrapFormMixin
User = get_user_model()

class CandidateProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CandidateProfile
        fields = ['resume', 'skills', 'bio','location']

class RecruiterProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'company_description', 'website']


class StyledAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    pass


class CustomUserCreationForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User   # <-- use your custom accounts.User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'candidate'  # Default role, can be changed later
        if commit:
            user.save()
        return user

class RecruiterSignupForm(BootstrapFormMixin, UserCreationForm):
    company = forms.CharField(max_length=255)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2", "company")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "recruiter"
        user.is_active = False   # require admin approval
        if commit:
            user.save()
            RecruiterProfile.objects.create(
                user=user, company_name=self.cleaned_data["company"]
            )
        return user
class StyledPasswordResetForm(BootstrapFormMixin, PasswordResetForm):
    pass


class StyledSetPasswordForm(BootstrapFormMixin, SetPasswordForm):
    pass