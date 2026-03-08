from datetime import timedelta

from django.utils import timezone
from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated

from ..users.permissions import Is_Seller
from .serializres import ProductSerializer,ProductCreateSerializer
from .models import Product



class ProductsListViews(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    
    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]
    
    search_fields = [
        'title',
        'description'
    ]

    ordering_fields = [
        'price',
        'created_at'
    ]
    
    
    def get_queryset(self):
        
        queryset = Product.objects.all()
        
        category = self.request.query_params.get("category")
        title = self.request.query_params.get("title")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        
        
        if category:
            queryset = queryset.filter(category__slug=category)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset
 

class ProductsGetOneViews(RetrieveAPIView):
    
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    
    queryset = Product.objects.all()
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        
        
        instance = self.get_object()
        
        
        Product.objects.filter(id=instance.id).update(view_count=F('view_count')+1)
    
        instance.refresh_from_db()
        
        serializer = self.get_serializer(instance)
        
        return Response(serializer.data)
    
    
class ProductsCreateViews(CreateAPIView):
    
    permission_classes = [IsAuthenticated,Is_Seller]
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.all()
    
    def perform_create(self, serializer):
        
        serializer.save(
            seller = self.request.user,
            expires_at=timezone.now() + timedelta(days=30)
        )
    
        
class ProductsUpdateViews(UpdateAPIView):
    
    permission_classes = [IsAuthenticated, Is_Seller]
    serializer_class = ProductCreateSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class ProductsDestroyViews(DestroyAPIView):
    
    permission_classes = [IsAuthenticated, Is_Seller]
    serializer_class = ProductCreateSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
    
    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {"detail": "Product deleted successfully"},
            status=status.HTTP_200_OK
        )


class ProductsPuplishViews(APIView):
    
    permission_classes = [IsAuthenticated, Is_Seller]
    
    def post(self, request:Request,id:int):
        
        product = get_object_or_404(
            Product,
            id=id,
            seller=request.user
        )
        
        if product.status != Product.Status.MODERATION:
            return Response(
                {"detail": "Product is not in moderation state"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.status = Product.Status.ACTIVE
        product.published_at = timezone.now()

        product.save(update_fields=["status", "published_at"])

        return Response(
            {"detail": "Product published successfully"},
            status=status.HTTP_200_OK
        )
        

class ProductsArchiveViews(APIView):

    permission_classes = [IsAuthenticated, Is_Seller]

    def post(self, request:Request, id: int):

        product = get_object_or_404(
            Product,
            id=id,
            seller=request.user
        )

        if product.status in [
            Product.Status.ARCHIVED,
            Product.Status.SOLD
        ]:
            return Response(
                {"detail": "Product cannot be archived"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.status = Product.Status.ARCHIVED
        product.save(update_fields=["status"])

        return Response(
            {"detail": "Product archived successfully"},
            status=status.HTTP_200_OK
        )
        
        
class ProductsSoldViews(APIView):
    
    permission_classes = [IsAuthenticated, Is_Seller]
    
    def post(self, request: Request, id: int):
        
        product = get_object_or_404(
            Product,
            id=id,
            seller=request.user
        )
        
        if product.status != Product.Status.ACTIVE:
            return Response(
                {"detail": "Only active products can be marked as sold"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.status = Product.Status.SOLD
        product.save(update_fields=["status"])

        return Response(
            {"detail": "Product marked as sold"},
            status=status.HTTP_200_OK
        )
        
    