from rest_framework import serializers

from .models import Category


class CategoriesListSerializer(serializers.ModelSerializer):
    
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "icon",
            "children"
        ]
        
    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategoriesListSerializer(children, many=True).data
        
        
        
        
