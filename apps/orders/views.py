from django.db import models
from django.db import transaction


from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderCreateSerializer,OrderStatusSerializer

class OrderListCreateView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = OrderCreateSerializer

    def get_queryset(self):

        user = self.request.user
        role = self.request.query_params.get("role")

        queryset = Order.objects.select_related(
            "product",
            "buyer",
            "seller"
        )

        if role == "seller":
            return queryset.filter(seller=user)

        if role == "buyer":
            return queryset.filter(buyer=user)

        return queryset.filter(
            models.Q(buyer=user) | models.Q(seller=user)
        ).order_by("-created_at")
        
        
class OrderDetailView(RetrieveAPIView):

    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return Order.objects.filter(
            models.Q(buyer=self.request.user) |
            models.Q(seller=self.request.user)
        )
        


class OrderStatusUpdateView(UpdateAPIView):

    serializer_class = OrderStatusSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

    def perform_update(self, serializer):

        with transaction.atomic():

            order = serializer.save()

            if order.status == Order.Status.PURCHASED:

                product = order.product

                product.status = "sotilgan"
                product.save(update_fields=["status"])

                order.seller.total_sales = models.F("total_sales") + 1
                order.seller.save(update_fields=["total_sales"])