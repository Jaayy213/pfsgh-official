from django.contrib import admin
from .models import BlogCategory, BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'total_views', 'unique_views')

    def unique_views(self, obj):
        return obj.pageviews.count()
    unique_views.short_description = 'Unique Visitors'


admin.site.register(BlogCategory)