from django.db import models

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