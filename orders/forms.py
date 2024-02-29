from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 
            'email', 
            'phone', 
            'address1', 
            'address2', 
            'country', 
            'county_region_state', 
            'city', 
            'zip_code', 
            'order_key'
        ]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product_inventory', 'quantity']