from django.db import models
from django.core.validators import FileExtensionValidator
import uuid

def generate_ref_number():
    return f"PFS-{uuid.uuid4().hex[:6].upper()}"

class ServiceRequest(models.Model):
    SERVICE_CHOICES = [
        ('A', 'Dehydrator / Drying Service Only'),
        ('B', 'Product Development Only'),
        ('C', 'Both - Product Development + Drying'),
    ]
    
    REGISTRATION_STATUS = [
        ('Registered', 'Registered'),
        ('Not Registered', 'Not Registered'),
        ('In Process', 'In Process'),
    ]

    CURRENT_FORM_CHOICES = [
        ('Whole', 'Whole'),
        ('Sliced', 'Sliced'),
        ('Crushed', 'Crushed'),
        ('Pitted', 'Pitted'),
        ('Powder', 'Powder'),
        ('Other', 'Other'),
    ]

    BUDGET_RANGES = [
        ('Below GHS 5k', 'Below GHS 5k'),
        ('5k-10k', '5k-10k'),
        ('10k-25k', '10k-25k'),
        ('Above 25k', 'Above 25k'),
    ]

    # Meta
    ref_number = models.CharField(max_length=20, unique=True, default=generate_ref_number, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    service_choice = models.CharField(max_length=1, choices=SERVICE_CHOICES)

    # SECTION 1: Client Info
    full_name_or_company = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    business_address = models.TextField()
    registration_status = models.CharField(max_length=20, choices=REGISTRATION_STATUS)

    # SECTION 2A: Drying Service (A or C)
    product_name = models.CharField(max_length=255, blank=True, null=True)
    quantity_margarine_buckets = models.PositiveIntegerField(blank=True, null=True)
    current_form = models.CharField(max_length=20, choices=CURRENT_FORM_CHOICES, blank=True, null=True)
    current_form_other = models.CharField(max_length=100, blank=True, null=True)
    is_sorted = models.BooleanField(default=False)
    is_cleaned = models.BooleanField(default=False)
    washing_needed_at_pfs = models.BooleanField(default=False)
    processing_method_details = models.TextField(blank=True, null=True)
    product_image = models.ImageField(upload_to='drying_products/', blank=True, null=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    has_dried_before = models.BooleanField(default=False)
    known_temperature = models.CharField(max_length=100, blank=True, null=True)
    known_time = models.CharField(max_length=100, blank=True, null=True)
    previous_result_good = models.BooleanField(default=False)
    pfs_decide_parameters = models.BooleanField(default=False)
    agree_sample_test = models.BooleanField(default=False)
    delivery_date = models.DateField(blank=True, null=True)
    confirm_delivery_before_10am = models.BooleanField(default=False)

    # SECTION 2B: Product Development (B or C)
    product_idea = models.TextField(blank=True, null=True)
    raw_materials_list = models.TextField(blank=True, null=True)
    current_production_method = models.TextField(blank=True, null=True)
    desired_product_form = models.JSONField(default=list, blank=True)
    packaging_preference = models.JSONField(default=list, blank=True)
    intended_pack_size = models.CharField(max_length=100, blank=True, null=True)
    target_retail_price = models.CharField(max_length=100, blank=True, null=True)
    storage_condition = models.CharField(max_length=50, blank=True, null=True)
    usage_method = models.CharField(max_length=100, blank=True, null=True)
    expected_shelf_life = models.CharField(max_length=100, blank=True, null=True)
    target_market = models.JSONField(default=list, blank=True)
    product_benefits = models.JSONField(default=list, blank=True)

    # SECTION 3: Additional Services Needed (B or C)
    additional_services = models.JSONField(default=list, blank=True)

    # SECTION 4: Project Parameters
    preferred_start_date = models.DateField()
    target_completion_date = models.DateField()
    indicative_budget = models.CharField(max_length=20, choices=BUDGET_RANGES)
    special_requirements = models.TextField(blank=True, null=True)

    # SECTION 5: Terms & Submit
    declaration_accepted = models.BooleanField(default=False)
    signature_typed_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ref_number} - {self.full_name_or_company}"