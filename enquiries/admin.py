from django.contrib import admin
from .models import Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "region",
        "company_name",
        "service_required",
        "phone_number",
        "email",
        "created_at",
    )

    list_filter = ("service_required", "social_platform", "created_at")
    search_fields = ("first_name", "last_name", "email", "company_name")
    ordering = ("-created_at",)