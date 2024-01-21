from django.contrib import admin
from django.urls import path, include
from .views import create_category, create_link, links, categories, edit_category, edit_link

urlpatterns = [
    path('create-category/', create_category, name='create-category'),
    path('create-link/', create_link, name='create-link'),
    path('', links, name='links'),
    path('categories/', categories, name='categories'),
    path('links/<int:pk>/edit/', edit_link, name='edit-link'),  
    path('categories/<int:pk>/edit/', edit_category, name='edit-category'),  # Corrected the spelling
]
