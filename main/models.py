from django.db import models
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Product Tag Model
class ProductTag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Product Tags'

    def __str__(self):
        return self.name


class ClientRegion(models.TextChoices):
    AHAFO = "AHAFO", "Ahafo"
    ASHANTI = "ASHANTI", "Ashanti"
    BONO = "BONO", "Bono"
    BONO_EAST = "BONO_EAST", "Bono East"
    CENTRAL = "CENTRAL", "Central"
    EASTERN = "EASTERN", "Eastern"
    GREATER_ACCRA = "GREATER_ACCRA", "Greater Accra"
    NORTH_EAST = "NORTH_EAST", "North East"
    NORTHERN = "NORTHERN", "Northern"
    OTI = "OTI", "Oti"
    SAVANNAH = "SAVANNAH", "Savannah"
    UPPER_EAST = "UPPER_EAST", "Upper East"
    UPPER_WEST = "UPPER_WEST", "Upper West"
    VOLTA = "VOLTA", "Volta"
    WESTERN = "WESTERN", "Western"
    WESTERN_NORTH = "WESTERN_NORTH", "Western North"
    DIASPORA = "DIASPORA", "Diaspora"


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/')
    description = models.TextField()
    region = models.CharField(max_length=20, choices=ClientRegion.choices, default=ClientRegion.GREATER_ACCRA)
    tag = models.ForeignKey(ProductTag, on_delete=models.SET_NULL, null=True, related_name='product_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product - {self.name}"
    


class AudioFile(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/')
    cover_image = models.ImageField(upload_to='audio/covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VideoFile(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='videos/thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

# Automatically delete actual audio files and covers from disk on database deletion
@receiver(post_delete, sender=AudioFile)
def auto_delete_audio_files_on_delete(sender, instance, **kwargs):
    # Delete the main audio file
    if instance.audio_file:
        if os.path.isfile(instance.audio_file.path):
            os.remove(instance.audio_file.path)
            
    # Delete the cover image if it exists
    if instance.cover_image:
        if os.path.isfile(instance.cover_image.path):
            os.remove(instance.cover_image.path)


# Automatically delete actual video files and thumbnails on database deletion
@receiver(post_delete, sender=VideoFile)
def auto_delete_video_files_on_delete(sender, instance, **kwargs):
    # Delete the main video file
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
            
    # Delete the thumbnail image if it exists
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)