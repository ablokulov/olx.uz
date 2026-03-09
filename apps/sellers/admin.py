from django.contrib import admin

from .models import SellerProfile

@admin.register(SellerProfile)
class SellerProfile(admin.ModelAdmin):
    
    list_display = (
        "id",
        "user",
        "shop_name",
        "shop_description",
        "rating"
    )