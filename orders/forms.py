from django import forms
from .models import Order, OrderItem

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 
            'email', 
            'phone_number', 
            'address_1', 
            'address_2', 
            'city', 
            'county_region', 
            'country', 
            'zip_code', 
            'total_paid',
        ]


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product_inventory', 'quantity']