from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('links/', include('links.urls')),
    path('', include('account.urls')),
    path('dashboard/', include('dashboard.urls')),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
]
