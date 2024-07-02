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
            'country', 
            'zip_code', 
        ]

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product_inventory', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'zip_code': 'Postal Code',
            'city': 'Town or City',
            'address_1': 'Street Address 1',
            'address_2': 'Street Address 2',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

        self.fields['country'].widget.attrs['title'] = "Country Selection"