from rest_framework import serializers
from django.db.models import Avg

from .models import Review
from apps.orders.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            "id",
            "order",
            "reviewer",
            "seller",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = (
            "reviewer",
            "seller",
            "created_at",
        )
        
class ReviewCreateSerializer(serializers.ModelSerializer):

    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        source="order"
    )

    class Meta:
        model = Review
        fields = [
            "order_id",
            "rating",
            "comment",
        ]
        
    def validate(self, attrs):

        order = attrs["order"]
        user = self.context["request"].user

        # 1. faqat buyer review yozishi mumkin
        if order.buyer != user:
            raise serializers.ValidationError(
                "Faqat buyurtma egasi fikr qoldira oladi"
            )

        # 2. order sotib olingan bo‘lishi kerak
        if order.status != Order.Status.PURCHASED:
            raise serializers.ValidationError(
                "Faqat sotib olingan buyurtma uchun fikr yozish mumkin"
            )

        # 3. review mavjud emasligini tekshirish
        if hasattr(order, "review"):
            raise serializers.ValidationError(
                "Bu buyurtma uchun fikr allaqachon yozilgan"
            )

        return attrs
    
    def create(self, validated_data):

        request = self.context["request"]
        order = validated_data["order"]

        review = Review.objects.create(
            order=order,
            reviewer=request.user,
            seller=order.seller,
            rating=validated_data["rating"],
            comment=validated_data["comment"],
        )

        # seller rating update
        avg_rating = Review.objects.filter(
            seller=order.seller
        ).aggregate(avg=Avg("rating"))["avg"]

        order.seller.rating = avg_rating
        order.seller.save(update_fields=["rating"])

        return review