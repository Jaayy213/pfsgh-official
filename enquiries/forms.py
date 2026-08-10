from django import forms
from .models import Enquiry, EnquiryComment

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['first_name', 'last_name', 'region', 'address', 'phone_number', 'email', 'company_name', 'promocode', 'service_required', 'social_platform', 'social_handle', 'service_type', 'other_enquiry']

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "region": forms.Select(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "promocode": forms.TextInput(attrs={"class": "form-control"}),
            "service_required": forms.Select(attrs={"class": "form-control"}),
            "social_platform": forms.Select(attrs={"class": "form-control"}),
            "social_handle": forms.TextInput(attrs={"class": "form-control"}),
            "service_type": forms.Select(attrs={"class": "form-control"}),
            "other_enquiry": forms.Textarea(attrs={"class": "form-control"}),
        }

        help_texts = {
            "first_name": "Enter your first name.",
            "last_name": "Enter your last name.",
            "region": "Select the region where you are located.",
            "address": "Provide your full address or nearest landmark.",
            "phone_number": "Include country code (e.g. +233...).",
            "email": "Enter a valid email address we can contact you on.",
            "company_name": "Enter your business or company name (if applicable).",
            "promocode": "Enter Promo Code or Referral Name",
            "service_required": "Select the service you are interested in.",
            "social_platform": "Choose your primary social media platform.",
            "social_handle": "Provide a full URL (e.g. https://instagram.com/yourhandle)",
            "service_type": "Choose between Regular, Express, and Premium Connect Services",
            "other_enquiry": "Add any additional details to help us better understand your request.",
        }


class EnquiryCommentForm(forms.ModelForm):
    class Meta:
        model = EnquiryComment
        fields = ['text']

        widgets = {
            "text": forms.TextInput(attrs={"class": "form-control"}),
        }

        help_texts = {
            "text": "Enter a comment.",
        }