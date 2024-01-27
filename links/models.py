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
    
    class Meta:
        ordering = ('name',)



class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Link(models.Model):
    STATUS_CHOICES = [
        ('default', 'Default'),
        ('need', 'Need'),
        ('finished', 'Finished'),
        ('go_back_to', 'Go Back To'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('canceled', 'Canceled'),
        ('pending_approval', 'Pending Approval'),
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('archived', 'Archived'),
    ]

    PRIORITY_CHOICES = [
        ('default', 'Default'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical'),
        ('normal', 'Normal'),
    ]

    name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, related_name='links', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='links', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='default')
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default='default')
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name