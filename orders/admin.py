from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('lineitem_total',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total_paid', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('order_number', 'user__username', 'user__email', 'full_name', 'phone_number', 'city', 'zip_code')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_inventory', 'quantity', 'lineitem_total')
    search_fields = ('order__order_number', 'product_inventory__product__name')
    readonly_fields = ('lineitem_total',)  # Ensure lineitem_total is read-only in admin
