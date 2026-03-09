from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..categories.models import Category
from .models import Product

CustomUser = get_user_model()


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'telegram_username', 'first_name']
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    
    seller = SellerSerializer(read_only=True)    
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'description',
            'condition',
            'price',
            'price_type',
            'region',
            'district',
            'view_count',
            'favorite_count',
            'status',
            'created_at',
            'updated_at',
            'published_at',
            'expires_at',
            'seller',
            'category'
            
        ]
        
class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "category",
            "title",
            "description",
            "condition",
            "price",
            "price_type",
            "region",
            "district"
        ]
        
    def validated_price(self,value):        
        if value is not None and value < 0:
            
            raise serializers.ValidationError('Price manfiy bo\'lishi mumkin emas')
        
        return value
                        
        