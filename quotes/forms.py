from django import forms
from .models import QuoteRequest

SERVICE_CHOICES = [
    ('business-plans', 'Business Plan Drafting'),
    ('certification', 'FDA & GSA Certification'),
    ('dehydration', 'Commercial Dehydration'),
    ('product-development', 'Product Development'),
    ('safety-training', 'Safety Training'),
    ('mango-powder', 'Mango Powder Products'),
    ('fruit-porridge', 'Fruit Fiber Porridge'),
    ('rice-porridge', 'Rice Porridge'),
]


class QuoteRequestForm(forms.ModelForm):
    firstName = forms.CharField(max_length=100, required=True)
    lastName = forms.CharField(max_length=100, required=True)
    projectDescription = forms.CharField(widget=forms.Textarea, required=True)
    additionalInfo = forms.CharField(widget=forms.Textarea, required=False)

    services = forms.MultipleChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={'required': 'Please select at least one service.'}
    )

    class Meta:
        model = QuoteRequest
        fields = [
            'email',
            'phone',
            'company',
            'industry',
            'services',
            'timeline',
            'budget',
            'priority',
        ]

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Assign camelCase fields to model attributes
        instance.first_name = self.cleaned_data['firstName']
        instance.last_name = self.cleaned_data['lastName']
        instance.project_description = self.cleaned_data['projectDescription']
        instance.additional_info = self.cleaned_data.get('additionalInfo', '')
        
        if commit:
            instance.save()
        return instance