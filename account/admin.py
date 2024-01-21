from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from .models import User, Plan
from .forms import ChangePlanForm

class ChangePlanForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['plan']

class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'plan',
        'is_staff',
        'is_superuser',
    )

    form = ChangePlanForm
    add_form = ChangePlanForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Plan', {'fields': ('plan',)}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'plan'),
        }),
    )

class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'max_num_links',
        'max_num_tag',
        'max_num_category',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Plan, PlanAdmin)
