from django.contrib import admin
from .models import Profile, Address

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'created_at', 'updated_at')
    search_fields = ('user__username', 'first_name', 'last_name')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('profile', 'address_line', 'city', 'country', 'county_region', 'zip_code', 'is_primary', 'phone_number', 'created_at', 'updated_at')
    list_filter = ('is_primary', 'country', 'created_at', 'updated_at')
    search_fields = ('profile__user__username', 'address_line', 'city', 'county_region', 'zip_code', 'phone_number')
