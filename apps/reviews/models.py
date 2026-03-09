from django.db import models
from django.contrib.auth import get_user_model

from ..orders.models import Order

CustomUser = get_user_model()


class Review(models.Model):

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="review")
    reviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews_given")
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews_received")
    rating = models.PositiveSmallIntegerField()

    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating} for {self.seller}"