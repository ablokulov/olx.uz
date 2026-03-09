from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import F

from .models import Favorite
from .serializers import FavoriteSerializer
from ..products.models import Product


class FavoriteListCreateView(ListCreateAPIView):

    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        product = serializer.validated_data["product"]

        favorite = serializer.save(user=self.request.user)

        Product.objects.filter(id=product.id).update(
            favorite_count=F("favorite_count") + 1
        )
        
class FavoriteDestroyView(DestroyAPIView):

    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):

        product = instance.product

        instance.delete()

        Product.objects.filter(id=product.id).update(
            favorite_count=F("favorite_count") - 1
        )