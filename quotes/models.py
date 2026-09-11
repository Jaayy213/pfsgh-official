from django.db import models


class QuoteRequest(models.Model):
    INDUSTRY_CHOICES = [
        ('food-beverage', 'Food & Beverage'),
        ('manufacturing', 'Manufacturing'),
        ('healthcare', 'Healthcare'),
        ('agriculture', 'Agriculture'),
        ('retail', 'Retail'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]

    TIMELINE_CHOICES = [
        ('urgent', 'Urgent (1-2 weeks)'),
        ('fast', 'Fast Track (3-4 weeks)'),
        ('standard', 'Standard (1-2 months)'),
        ('flexible', 'Flexible (2+ months)'),
    ]

    BUDGET_CHOICES = [
        ('500-1000', 'GHC500 - GHC1,000'),
        ('1500-2500', 'GHC1,500 - GHC2,500'),
        ('3000-5000', 'GHC3,000 - GHC5,000'),
        ('over-5000', 'Over GHC5,000'),
        ('discuss', 'Prefer to discuss'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    # Personal / Contact Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    company = models.CharField(max_length=150)
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES, blank=True, null=True)

    # Services (Array / List of selected service keys)
    services = models.JSONField(
        default=list,
        help_text="Selected services list"
    )

    # Project Details
    project_description = models.TextField()
    timeline = models.CharField(max_length=50, choices=TIMELINE_CHOICES, blank=True, null=True)
    budget = models.CharField(max_length=50, choices=BUDGET_CHOICES, blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quote Request'
        verbose_name_plural = 'Quote Requests'

    def __str__(self):
        return f"Quote Request: {self.first_name} {self.last_name} ({self.company})"