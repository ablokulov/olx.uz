from django.contrib import admin
from .models import Favorite


# admin.site.register(Favorite)
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "product",
        "created_at",
    )

    list_select_related = (
        "user",
        "product",
    )

    search_fields = (
        "user__username",
        "product__title",
    )

    list_filter = (
        "created_at",
    )

    ordering = ("-created_at",)