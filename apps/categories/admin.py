from django.contrib import admin

from .models import Category


# admin.site.register(Category)
# Register your models here.

@admin.register(Category)
class Category(admin.ModelAdmin):
    
    list_display = (
        "id",
        "name",
        "slug",
        "is_active"
    )