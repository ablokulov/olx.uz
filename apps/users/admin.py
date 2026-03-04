from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "id",
        "telegram_id",
        "telegram_username",
        "role",
        "phone_number",
        "avatar_preview",
        "is_active",
        "is_staff",
        "date_joined",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "telegram_id",
        "telegram_username",
        "phone_number",
    )

    ordering = ("-date_joined",)

    readonly_fields = (
        "avatar_preview",
        "date_joined",
        "last_login",
    )

    fieldsets = (
        ("Telegram Info", {
            "fields": (
                "telegram_id",
                "telegram_username",
            )
        }),

        ("Profile", {
            "fields": (
                "first_name",
                "last_name",
                "phone_number",
                "avatar",
                "avatar_preview",
                "role",
            )
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),

        ("Important dates", {
            "fields": (
                "last_login",
                "date_joined",
            )
        }),
    )
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50"/>',
                obj.avatar.url
            )
        return "-"