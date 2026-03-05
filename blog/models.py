from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
import math
from django.conf import settings
from django.utils import timezone

# Blog Category Model
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name

# Blog Post Model
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    period = models.DateField(default=timezone.now)
    read_time = models.PositiveIntegerField(editable=False)
    excerpt = models.TextField()
    content = CKEditor5Field(config_name='default')
    image = models.ImageField(upload_to="blog_images/")
    total_views = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)

    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def estimate_read_time(self):
        words_per_minute = 200
        text = self.content
        word_count = len(text.split())
        return math.ceil(word_count / words_per_minute)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        self.read_time = self.estimate_read_time()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    
# Model to Count Page Views
class BlogPageView(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="pageviews")
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=40, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ('post', 'ip_address', 'session_key')
    

# Comments Model
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} on {self.post}"