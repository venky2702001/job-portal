from django import forms
from .models import Application
from jobportal.formutils import BootstrapFormMixin

class ApplicationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']
