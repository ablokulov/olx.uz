from django.utils import timezone

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from ..products.models import Product
from ..products.serializers import ProductSerializer
from .serializers import CategoriesListSerializer
from .models import Category


class CategoriesListViews(ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related("children")
    serializer_class = CategoriesListSerializer
    permission_classes = [AllowAny]


class CategoriesDetailViews(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesListSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
        
        
        
class CategoryProductsListView(ListAPIView):

    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        slug = self.kwargs.get("slug")

        queryset = Product.objects.filter(
            category__slug=slug,
            status=Product.Status.ACTIVE,
            expires_at__gt=timezone.now()
        ).select_related(
            "category",
            "seller"
        ).prefetch_related(
            "images"
        )

        return queryset
  