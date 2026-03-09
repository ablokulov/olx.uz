from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewListCreateView(ListCreateAPIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        seller_id = self.request.query_params.get("seller_id")

        queryset = Review.objects.select_related(
            "order",
            "reviewer",
            "seller"
        )

        if seller_id:
            queryset = queryset.filter(seller_id=seller_id)

        return queryset

    def get_serializer_class(self):

        if self.request.method == "POST":
            return ReviewCreateSerializer

        return ReviewSerializer