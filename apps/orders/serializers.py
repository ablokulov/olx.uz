from rest_framework import serializers
from .models import Order
from apps.products.models import Product


class OrderCreateSerializer(serializers.ModelSerializer):

    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product"
    )

    class Meta:
        model = Order
        fields = ["id", "product_id", "notes"]

    def create(self, validated_data):

        request = self.context["request"]
        product = validated_data["product"]

        return Order.objects.create(
            product=product,
            buyer=request.user,
            seller=product.seller,
            final_price=product.price,
            notes=validated_data.get("notes", "")
        )
        
class OrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "status",
            "meeting_location",
            "meeting_time"
        ]

    def validate(self, attrs):

        order = self.instance
        user = self.context["request"].user
        new_status = attrs.get("status")

        if user == order.seller:

            if order.status != Order.Status.WAITING:
                raise serializers.ValidationError("Seller faqat WAITING orderni ozgartira oladi")

        elif user == order.buyer:

            if order.status != Order.Status.AGREED:
                raise serializers.ValidationError("Buyer faqat AGREED orderni yakunlay oladi")

        else:
            raise serializers.ValidationError("Ruxsat yuq")

        return attrs
    