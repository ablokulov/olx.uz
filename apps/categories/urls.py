from django.urls import path

from .views import CategoriesListViews, CategoriesDetailViews, CategoriesDetailProducts


urlpatterns = [
    path("categories/", CategoriesListViews.as_view(), name="categories"),
    path("categories/<slug:slug>/", CategoriesDetailViews.as_view(),name="categories_slug"),
    path("categories/<slug:slug>/products/", CategoriesDetailProducts.as_view(), name="categories_products")
]