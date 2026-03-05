from django.urls import path

from .views import CategoriesListViews, CategoriesDetailViews


urlpatterns = [
    path("categories/", CategoriesListViews.as_view(), name="categories"),
    path("categories/<int:slug>/", CategoriesDetailViews.as_view(),name="categories_slug")
]