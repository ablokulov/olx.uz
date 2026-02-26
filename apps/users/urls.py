from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserTelegramloginViews, UserLogoutViews


urlpatterns = [
    path("auth/telegram-login/", UserTelegramloginViews.as_view(),name="telegram-login/register"),
    path("auth/refresh/", TokenRefreshView.as_view(),name="refresh-token" ),
    path("auth/logout/", UserLogoutViews.as_view(), name="logout")
]

