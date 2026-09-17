from django import forms
from .models import ServiceRequest


class ServiceRequestForm(forms.ModelForm):
    # Options for JSONField multi-selects
    DESIRED_FORM_CHOICES = [
        ('Powder', 'Powder'),
        ('Paste', 'Paste'),
        ('Granules', 'Granules'),
        ('Liquid', 'Liquid'),
        ('Dried Slices', 'Dried Slices'),
        ('Other', 'Other'),
    ]

    PACKAGING_CHOICES = [
        ('Pouches / Squeezables', 'Pouches / Squeezables'),
        ('Jars / Bottles', 'Jars / Bottles'),
        ('Sachets', 'Sachets'),
        ('Boxes / Cartons', 'Boxes / Cartons'),
        ('Bulk Containers', 'Bulk Containers'),
    ]

    TARGET_MARKET_CHOICES = [
        ('Local Retail', 'Local Retail'),
        ('Supermarkets', 'Supermarkets'),
        ('Export / International', 'Export / International'),
        ('B2B / Wholesale', 'B2B / Wholesale'),
    ]

    BENEFITS_CHOICES = [
        ('Nutritional / Health', 'Nutritional / Health'),
        ('Convenience / Ready-to-use', 'Convenience / Ready-to-use'),
        ('Extended Shelf-life', 'Extended Shelf-life'),
        ('Cost Effective', 'Cost Effective'),
    ]

    ADDITIONAL_SERVICES_CHOICES = [
        ('FDNC / FDA Registration Support', 'FDNC / FDA Registration Support'),
        ('Nutritional Analysis / Lab Testing', 'Nutritional Analysis / Lab Testing'),
        ('Packaging & Label Design', 'Packaging & Label Design'),
        ('Shelf-life Determination', 'Shelf-life Determination'),
        ('Recipe Standardization', 'Recipe Standardization'),
    ]

    # Explicit JSONField Multi-Select Definitions
    desired_product_form = forms.MultipleChoiceField(
        choices=DESIRED_FORM_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    packaging_preference = forms.MultipleChoiceField(
        choices=PACKAGING_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    target_market = forms.MultipleChoiceField(
        choices=TARGET_MARKET_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    product_benefits = forms.MultipleChoiceField(
        choices=BENEFITS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )
    additional_services = forms.MultipleChoiceField(
        choices=ADDITIONAL_SERVICES_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    class Meta:
        model = ServiceRequest
        fields = '__all__'
        exclude = ['ref_number', 'created_at']

        widgets = {
            # Meta / Main Selector
            'service_choice': forms.RadioSelect(attrs={'class': 'btn-check'}),

            # SECTION 1: Client Information
            'full_name_or_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name or company name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 020 793 5696'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com'
            }),
            'business_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Physical business address or location'
            }),
            'registration_status': forms.Select(attrs={'class': 'form-select'}),

            # SECTION 2A: Drying Service (A or C)
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Mango, Cassava, Chili'
            }),
            'quantity_margarine_buckets': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estimated number of buckets'
            }),
            'current_form': forms.Select(attrs={'class': 'form-select'}),
            'current_form_other': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Specify if Other'
            }),
            'is_sorted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_cleaned': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'washing_needed_at_pfs': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'processing_method_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Describe current preparation or slicing method'
            }),
            'product_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'has_dried_before': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'known_temperature': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 60°C'
            }),
            'known_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 12 hours'
            }),
            'previous_result_good': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pfs_decide_parameters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'agree_sample_test': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'delivery_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'confirm_delivery_before_10am': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            # SECTION 2B: Product Development (B or C)
            'product_idea': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your product concept, taste profile, and idea'
            }),
            'raw_materials_list': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'List key raw materials and ingredients required'
            }),
            'current_production_method': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'How do you currently make it (if applicable)?'
            }),
            'intended_pack_size': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 250g, 1 Litre'
            }),
            'target_retail_price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., GHS 50 per unit'
            }),
            'storage_condition': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Ambient, Refrigerated, Frozen'
            }),
            'usage_method': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Ready to eat, Mix with warm water'
            }),
            'expected_shelf_life': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 6 months, 1 year'
            }),

            # SECTION 4: Project Parameters
            'preferred_start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'target_completion_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'indicative_budget': forms.Select(attrs={'class': 'form-select'}),
            'special_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any allergen concerns, specific certifications, or handling notes'
            }),

            # SECTION 5: Terms & Confirmation
            'declaration_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'signature_typed_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Type your full legal name as digital signature'
            }),
        }