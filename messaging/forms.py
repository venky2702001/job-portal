# messaging/forms.py
from django import forms
from .models import Message
from jobportal.formutils import BootstrapFormMixin

class MessageForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ["recipient", "subject", "body"]
