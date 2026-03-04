from rest_framework import serializers

from .models import SellerProfile

class SellerDetailSerializer(serializers.ModelSerializer):

    telegram_username = serializers.CharField(source="user.telegram_username")

    class Meta:
        model = SellerProfile
        fields = [
            "id",
            "shop_name",
            "shop_description",
            "shop_logo",
            "region",
            "district",
            "address",
            "rating",
            "total_sales",
            "telegram_username",
        ]