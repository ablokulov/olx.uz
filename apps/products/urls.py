from django.urls import path

from .views import (
    ProductsListViews,
    ProductsGetOneViews,
    ProductsCreateViews,
    ProductsUpdateViews,
    ProductsDestroyViews,
    ProductsPuplishViews,
    ProductsArchiveViews,
    ProductsSoldViews,
    ProductImageListCreateView,
    ProductImageDetailView
)



urlpatterns = [
    path('products/', ProductsListViews.as_view(), name='products_list'),
    path('products/<int:id>/', ProductsGetOneViews.as_view(), name='product_getone'),
    path('products/create/', ProductsCreateViews.as_view(), name='product_create'),
    path('products/<int:id>/update/', ProductsUpdateViews.as_view(), name='product_update'),
    path('products/<int:id>/delete/', ProductsDestroyViews.as_view(), name='product_delete'),
    path('products/<int:id>/publish/', ProductsPuplishViews.as_view(), name='product_publish'),
    path('products/<int:id>/archive/', ProductsArchiveViews.as_view(), name='product_archive'),
    path('products/<int:id>/sold/', ProductsSoldViews.as_view(), name='product_sold'),
    path('products/<int:id>/images/', ProductImageListCreateView.as_view(), name='product-images' ),
    path('product-images/<int:id>/', ProductImageDetailView.as_view()),
]