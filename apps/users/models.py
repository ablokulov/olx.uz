from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager



class CustomUserManager(UserManager):
    
    def create_user(self,telegram_id,**extra_fields):
        if not telegram_id:
            raise ValueError("telegram_id required")
        
        user = self.model(telegram_id=telegram_id,**extra_fields)
        user.set_unasable_password()
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self,telegram_id, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        return self.create_user(telegram_id=telegram_id, **extra_fields)
     

class CustomUser(AbstractUser):
    
    username = None
    
    class Role(models.TextChoices):
        CUSTOMER = "customer","Xaridor"
        SELLER = "seller", "Sotuvchi"
        
    telegram_id = models.BigIntegerField(unique=True)
    telegram_username = models.CharField(max_length=150,blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10,default=Role.CUSTOMER, choices=Role.choices)
    avatar = models.ImageField(upload_to="users/images/",blank=True,null=True)
    
    USERNAME_FIELD = "telegram_id"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.telegram_id} - {self.telegram_username} ({self.role})"
    
    
    
    @property
    def is_seller(self):
        return self.role == self.Role.SELLER
    
    
    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER
    