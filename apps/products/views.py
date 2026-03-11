from datetime import timedelta

from django.utils import timezone
from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView, 
    CreateAPIView, 
    UpdateAPIView, 
    DestroyAPIView,
    ListCreateAPIView
    
)

from rest_framework.permissions import AllowAny,IsAuthenticated
from drf_spectacular.utils import extend_schema,OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from ..users.permissions import Is_Seller
from .serializers import ProductSerializer,ProductCreateSerializer,ProductImageSerializer,ProductImageUpdateSerializer
from .models import Product, ProductImage


from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Product
from .serializers import ProductSerializer

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="category",
            description="Category ID yoki slug",
            required=False,
            type=OpenApiTypes.STR
        ),
        OpenApiParameter(
            name="region",
            description="Product region",
            required=False,
            type=OpenApiTypes.STR
        ),
        OpenApiParameter(
            name="min_price",
            description="Minimal price",
            required=False,
            type=OpenApiTypes.INT
        ),
        OpenApiParameter(
            name="max_price",
            description="Maximum price",
            required=False,
            type=OpenApiTypes.INT
        ),
    ]
)


class ProductsListViews(ListAPIView):
    
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [
        "title",
        "description"
    ]

    ordering_fields = [
        "price",
        "created_at",
        "view_count"
    ]

    ordering = ["-created_at"]


    def get_queryset(self):

        queryset = Product.objects.filter(
            status=Product.Status.ACTIVE
        ).select_related("category", "seller")


        category = self.request.query_params.get("category")
        region = self.request.query_params.get("region")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")


        if category:
            if category.isdigit():
                queryset = queryset.filter(category_id=category)
            else:
                queryset = queryset.filter(category__slug=category)


        if region:
            queryset = queryset.filter(region__iexact=region)


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
        

class ProductImageListCreateView(ListCreateAPIView):

    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated, Is_Seller]

    def get_queryset(self):

        product_id = self.kwargs.get("product_id")

        return ProductImage.objects.select_related(
            "product"
        ).filter(
            product_id=product_id
        ).order_by("order")

    def perform_create(self, serializer):

        product_id = self.kwargs.get("product_id")

        product = get_object_or_404(Product, id=product_id)

        if product.seller != self.request.user:
            raise PermissionDenied("Bu product sizga tegishli emas")

    
        images_count = ProductImage.objects.filter(product=product).count()

        if images_count >= 10:
            raise PermissionDenied("Maksimal 10 ta rasm yuklash mumkin")

        serializer.save(product=product)
        
        
class ProductImageUpdateView(UpdateAPIView):

    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated, Is_Seller]
    queryset = ProductImage.objects.select_related("product")
    lookup_field = "id"

    def perform_update(self, serializer):

        image = self.get_object()

        if image.product.seller != self.request.user:
            raise PermissionDenied("Bu rasm sizga tegishli emas")

        is_main = serializer.validated_data.get("is_main")

        if is_main:
            ProductImage.objects.filter(
                product=image.product,
                is_main=True
            ).exclude(id=image.id).update(is_main=False)

        serializer.save()
        
        
class ProductImageDeleteView(DestroyAPIView):

    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticated, Is_Seller]
    queryset = ProductImage.objects.select_related("product")
    lookup_field = "id"

    def perform_destroy(self, instance):

        if instance.product.seller != self.request.user:
            raise PermissionDenied("Bu rasm sizga tegishli emas")

        instance.image.delete(save=False)  # media faylni o‘chirish
        instance.delete()