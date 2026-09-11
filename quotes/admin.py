from django.contrib import admin
from .models import QuoteRequest


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'email', 'phone', 'priority', 'created_at', 'is_processed')
    list_filter = ('priority', 'is_processed', 'industry', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'company', 'project_description')
    readonly_fields = ('created_at',)
    list_editable = ('is_processed',)