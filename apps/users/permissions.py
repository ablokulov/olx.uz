from rest_framework.permissions import BasePermission


class Is_Seller(BasePermission):
    message = "Faqat sotuvchilar uchun ruxsat berilgan."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_seller
    
    
    
class Is_Customer(BasePermission):
    message = "Faqat xaridorlar uchun ruxsat berilgan."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_customer
    