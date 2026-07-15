from django.contrib import admin
from .models import Product, ProductTag

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductTag)