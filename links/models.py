from django.db import models
from account.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Link(models.Model):
    STATUS_CHOICES = [
        ('need', 'Need'),
        ('finished', 'Finished'),
        ('go_back_to', 'Go Back To'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='links', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='links', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='need')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='medium')

    def __str__(self):
        return self.name