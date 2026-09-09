# interviews/forms.py
from django import forms
from .models import Interview
from jobportal.formutils import BootstrapFormMixin

class InterviewForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Interview
        fields = ["candidate", "job", "scheduled_at", "location", "notes"]
        widgets = {
            "scheduled_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, recruiter=None, **kwargs):
        super().__init__(*args, **kwargs)
        if recruiter is not None:
            # Local imports avoid a circular import between the apps
            from jobs.models import Job
            from applications.models import Application

            self.fields["job"].queryset = Job.objects.filter(recruiter=recruiter)
            candidate_ids = Application.objects.filter(
                job__recruiter=recruiter
            ).values_list("candidate_id", flat=True).distinct()
            User = self.fields["candidate"].queryset.model
            self.fields["candidate"].queryset = User.objects.filter(id__in=candidate_ids)
