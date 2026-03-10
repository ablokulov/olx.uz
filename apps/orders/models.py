from django.db import models
from django.contrib.auth import get_user_model

from ..products.models import Product

CustomUser = get_user_model()



    

class Order(models.Model):
    
    class Status(models.TextChoices):
        WAITING = 'kutilyapti', 'Kutilyapti'
        AGREED = 'kelishilgan', 'Kelishilgan'
        PURCHASED = 'sotib olingan', 'Sotib olingan'
        CANCELED = 'bekor qilingan', 'Bekor qilingan'
        
        
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders_buyer')
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders_seller')
    final_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.WAITING)
    meeting_location = models.CharField(max_length=255,blank=True)
    meeting_time = models.DateTimeField(null=True,blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product}"
    
    
    