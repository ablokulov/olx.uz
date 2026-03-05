
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

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
        
        
        
class CategoriesDetailProducts(ListAPIView):
    permission_classes = [AllowAny]
  