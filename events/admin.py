from django.contrib import admin
from .models import RSVP


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    # Display columns in the admin list view
    list_display = (
        'full_name',
        'email',
        'phone',
        'company',
        'job_title',
        'attendance_status',
        'created_at',
    )

    # Sidebar filters for quick navigation
    list_filter = (
        'attendance',
        'created_at',
    )

    # Fields searchable via the top search bar
    search_fields = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'company',
        'job_title',
    )

    # Read-only fields in detail view
    readonly_fields = ('created_at',)

    # Group fields into structured sections in detail view
    fieldsets = (
        ('Personal Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('company', 'job_title')
        }),
        ('RSVP Response', {
            'fields': ('attendance', 'dietary_requirements')
        }),
        ('System Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    # Pagination count per page
    list_per_page = 25

    # Custom methods for cleaner list view display
    @admin.display(description='Full Name', ordering='first_name')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @admin.display(description='Attendance', ordering='attendance')
    def attendance_status(self, obj):
        return obj.get_attendance_display()