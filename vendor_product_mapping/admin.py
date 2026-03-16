from django.contrib import admin
from .models import VendorProductMapping

@admin.register(VendorProductMapping)
class VendorProductMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'child', 'primary_mapping', 'is_active', 'created_at', 'updated_at')
    list_filter = ('primary_mapping', 'is_active')
    search_fields = ('parent__name', 'child__name')
