from django import forms
from .models import RSVP


class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'company',
            'job_title',
            'attendance',
            'dietary_requirements',
        ]