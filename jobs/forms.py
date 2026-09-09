from django import forms
from .models import Job
from jobportal.formutils import BootstrapFormMixin

class JobForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location', 'salary']
