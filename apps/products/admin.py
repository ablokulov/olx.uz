from django.contrib import admin

from .models import Product, ProductImage

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = (
        "id",
        "title"
    )
    
@admin.register(ProductImage)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = (
        "id",
        "product",
        "image"
    )

