from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from ..products.models import Product
from ..products.serializers import ProductSerializer
from .models import SellerProfile
from .serializers import SellerProfileSerializer,SellerDetailSerializer
from ..users.models import CustomUser


class SellerProfileView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request: Request):
        
        user = request.user
        
        if hasattr(user, "seller_profile"):
            return Response(
                {"detail": "Seller profile already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
        
        serializer = SellerProfileSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        seller = serializer.save(user=user)
        
        user.role = CustomUser.Role.SELLER
        
        user.save(update_fields=["role"])
        
        return Response(
            {
                "message": "Seller profile created",
                "seller_id": seller.id
            },
            status=status.HTTP_201_CREATED
        )
        

class SellerDetailViews(RetrieveAPIView):

    serializer_class = SellerDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
    lookup_url_kwarg = "profile_id"

    queryset = SellerProfile.objects.select_related("user")
    
 
class SellerProductsListView(ListAPIView):

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        seller_id = self.kwargs.get("seller_id")

        queryset = Product.objects.filter(
            seller_id=seller_id,
            status=Product.Status.ACTIVE
        ).select_related(
            "category",
            "seller"
        ).prefetch_related(
            "images"
        )
        
        return queryset

        