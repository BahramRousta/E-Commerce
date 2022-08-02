from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('book.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('comment_section.urls')),
    path('', include('shop.urls')),
    path('', include('cart.urls')),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

