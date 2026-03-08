from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator

from ..categories.models import Category


CustomUser = get_user_model()



class Product(models.Model):
    
    class Condition(models.TextChoices):
        NEW = 'yangi','Yangi'
        IDEAL = 'ideal', 'Ideal'
        GOOD = 'yaxshi', 'Yaxshi'
        STATISFACTORY = 'qoniqarli', 'Qoniqarli'
    
    class Price_Type(models.TextChoices):
        STRICT = 'qatiy', 'Qatiy'
        AGREED = 'kelishiladi', 'Kelishiladi'
        FREE   = 'bepul', 'Bepul'
        EXCHANGE = 'ayirboshlash', 'Ayirboshlash'
        
    class Status(models.TextChoices):
        MODERATION = 'moderatsiyada', 'Moderatsiyada'
        ACTIVE = 'aktiv', 'Aktiv'
        REJECTED = 'rad etilgan', 'Rad etilgan'
        SOLD = 'sotilgan', 'Sotilgan'
        ARCHIVED = 'arxivlangan', 'Arxivlangan'
        
        
    seller = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name="products")
    title = models.CharField(max_length=200)
    description = models.TextField()
    condition = models.CharField(max_length=30,choices=Condition.choices,default=Condition.GOOD)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,validators=[MinValueValidator(0, message="Narx manfiy bo'lishi mumkin emas")])
    price_type = models.CharField(max_length=30,choices=Price_Type.choices,default=Price_Type.AGREED)
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    view_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=30,choices=Status.choices, default=Status.MODERATION)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True,blank=True,)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=30)

        super().save(*args, **kwargs)
    
    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at'])
        ]
        
    def __str__(self):
        return self.title
    
    
class ProductImage(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/images/")
    order = models.PositiveIntegerField(default=0)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):

        if self.is_main:
            ProductImage.objects.filter(product=self.product).update(is_main=False)

        super().save(*args, **kwargs)

    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"{self.product.title} image"
    
    
    
    
    
    
    
    