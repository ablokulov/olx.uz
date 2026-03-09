from rest_framework import serializers

from .models import CustomUser




class UserTelegramloginSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    username = serializers.CharField(max_length=150, required=False, allow_blank=True)
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    photo_url = serializers.URLField(required=False, allow_blank=True)
    
    
class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "telegram_id",
            "telegram_username",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "avatar",
            "is_active",
            "date_joined",
        ]