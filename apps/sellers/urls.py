from django.urls import path

from .views import SellerProfileView,SellerDetailViews,SellerProductsListView


urlpatterns = [
    
    path('users/me/upgrade-to-seller/', SellerProfileView.as_view(),name='seller_create_profile'),
    path('sellers/<int:seller_id>/', SellerDetailViews.as_view(), name='seller_detail'),
    path('sellers/<int:seller_id>/products/', SellerProductsListView.as_view(), name='seller_detail_product')
]