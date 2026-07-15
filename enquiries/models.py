from django.db import models

class Enquiry(models.Model):
    SERVICE_TYPE_CHOICES = [
        ("regular", "Regular"),
        ("express", "Express"),
        ("premium_connect", "Premium Connect"),
    ]

    SERVICE_CHOICES = [
        ("gsa_fda", "GSA & FDA Registration"),
        ("business_plan", "Business Plan"),
        ("product_dev", "Product Development"),
        ("product_dehydration", "Product Dehydration"),
        ("business_registration", "Business Registration Certificate"),
        ("machinery", "Machinery Sourcing"),
        ("consultation", "General Consultation"),
        ("facility_setup", "Comprehensive Facility Setup Proposal"),
        ("other", "Other"),
    ]

    SOCIAL_CHOICES = [
        ("instagram", "Instagram"),
        ("tiktok", "TikTok"),
        ("snapchat", "Snapchat"),
        ("x", "X (Twitter)"),
        ("facebook", "Facebook"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
    ("new", "New"),
    ("contacted", "Contacted"),
    ("closed", "Closed"),
    ("not_reachable", "Not Reachable"),
    ("service_declined", "Service Declined"),
    ]

    REGIONS_CHOICES = [
        ("ahafo", "Ahafo Region"),
        ("ashanti", "Ashanti Region"),
        ("bono", "Bono Region"),
        ("bono_east", "Bono East Region"),
        ("central", "Central Region"),
        ("eastern", "Eastern Region"),
        ("greater_accra", "Greater Accra Region"),
        ("north_east", "North East Region"),
        ("northern", "Northern Region"),
        ("oti", "Oti Region"),
        ("savannah", "Savannah Region"),
        ("upper_east", "Upper East Region"),
        ("upper_west", "Upper West Region"),
        ("volta", "Volta Region"),
        ("western", "Western Region"),
        ("western_north", "Western North Region"),
    ]


    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    region = models.CharField(
        max_length=25,
        choices=REGIONS_CHOICES
    )
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    company_name = models.CharField(max_length=255)

    promocode = models.CharField(max_length=250, default="NONE")

    service_required = models.CharField(
        max_length=50,
        choices=SERVICE_CHOICES
    )

    service_type = models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        default="regular"
    )

    social_platform = models.CharField(
        max_length=50,
        choices=SOCIAL_CHOICES,
        blank=True,
        null=True
    )

    social_handle = models.URLField()

    other_enquiry = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

    def __str__(self):
        return self.full_name