from django.contrib import admin
from .models import VendorProfile, CustomerProfile

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'user', 'phone']
    search_fields = ['shop_name', 'user__username']


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    search_fields = ['user__username']
