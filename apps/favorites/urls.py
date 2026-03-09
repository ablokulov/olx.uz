from django.urls import path

from .views import FavoriteListCreateView, FavoriteDestroyView

urlpatterns = [
    path('favorites/', FavoriteListCreateView.as_view(), name='favorites'),
    path('favorites/<int:id>', FavoriteDestroyView.as_view(), name='favorites_destroy')
]