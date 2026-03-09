from django.db import models
from django.contrib.auth import get_user_model


from ..products.models import Product

CustomUser = get_user_model()


class Favorite(models.Model):
    
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='favorite')
    prooduct = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='favorite_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user}_{self.product}"
    
    
