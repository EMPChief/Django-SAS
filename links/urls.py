from django.contrib import admin
from django.urls import path, include
from .views import create_category, create_link

urlpatterns = [
    path('create-category/', create_category, name='create-category'),
    path('create-link/', create_link, name='create-link'),
]
