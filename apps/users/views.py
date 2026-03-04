from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


from .serializers import UserTelegramloginSerializer, UserLogoutSerializer, MeSerializer
from .models import CustomUser



class UserTelegramloginViews(APIView):
    permission_classes = [AllowAny]
    
    def post(self,request:Request):
        serializer = UserTelegramloginSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
            
        telegram_id = data["telegram_id"]
        username    = data.get("username", "") or str(telegram_id)
        first_name  = data.get("first_name", "")
        last_name   = data.get("last_name", "")
            
            
        user, created = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "telegram_username":username,
                "first_name": first_name,
                "last_name": last_name,
                "role": CustomUser.Role.CUSTOMER
            }
        )

        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
        
      
      
class UserLogoutViews(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request:Request):
        serializer = UserLogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        refresh_token = data['refresh']
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
        except TokenError as e:
            
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Muvaffaqiyatli chiqdingiz."}
        )
            
        
        
        
class MeViews(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request:Request):
        serializer = MeSerializer(request.user)
        
        return Response(serializer.data)
        
    def patch(self, request:Request):
        serializer = MeSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
    
        
        
        
        
        
   