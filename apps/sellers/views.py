from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import SellerProfile
from .serializers import SellerDetailSerializer


class SellerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request: Request):
        return Response("Ok")



class SellerDetailViews(generics.RetrieveAPIView):
    
    queryset = SellerProfile.objects.all()
    serializer_class = SellerDetailSerializer()
    permission_classes = [AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = 'seller_id'
    
 
class SellerDetailProductViews(APIView):
    permission_classes = [AllowAny]
    def get(self, request: Request, seller_id: int):
        pass