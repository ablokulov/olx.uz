
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView,SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.sellers.urls')),
    path('api/v1/', include('apps.categories.urls')),
    path('api/v1/', include('apps.products.urls')),
    path('api/v1/', include('apps.favorites.urls')),
    path('api/v1/', include('apps.orders.urls')),
    path('api/v1/', include('apps.reviews.urls')),
    
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )





