from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    register,
    custom_login,
    custom_logout,
    checkout,
    create_sub,
    complete,
    cancel,
)

urlpatterns = [
    path('register/', register, name='register'),
    path('logout/', custom_logout, name='logout'),
    path('login/', custom_login, name='login'),
    path('checkout/', checkout, name='checkout'),
    path('create-sub/', create_sub, name='create_sub'),
    path('complete/', complete, name='complete'),
    path('cancel/', cancel, name='cancel'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
