from django.contrib import admin
from .models import Category, Link


class LinkInline(admin.TabularInline):
    model = Link
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_by', 'created_at', 'links_count')
    search_fields = ('name', 'description', 'created_by__username')
    list_select_related = ('created_by',)
    inlines = [LinkInline]

    def links_count(self, obj):
        return obj.links.count()
    links_count.short_description = 'Links Count'



class LinkAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'url', 'category', 'created_by', 'created_at', 'status', 'priority', 'is_active'
    )
    list_filter = ('status', 'priority')
    search_fields = ('name', 'url', 'description', 'created_by__username')
    list_select_related = ('created_by', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Link, LinkAdmin)
