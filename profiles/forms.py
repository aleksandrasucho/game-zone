from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Profile, Address
from django_countries import countries

class ProfileForm(forms.ModelForm):
    """Form for the Profile model."""
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture']
        help_texts = {
            'first_name': '',  # Remove help text for first_name
            'last_name': '',   # Remove help text for last_name
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last name',
                }
            ),
            'profile_picture': forms.HiddenInput(),  # Hide the profile picture input
        }


class AddressForm(forms.ModelForm):
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={'class': 'form-control'}),
        choices=countries  # Provide the list of countries
    )

    class Meta:
        model = Address
        fields = [
            'country',
            'county_region',
            'city',
            'address_line',
            'zip_code',
            'phone_number',
            'is_primary'
        ]
        help_texts = {
            field: '' for field in fields  # Remove help text for all fields
        }
        widgets = {
            'county_region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'County/Region'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'address_line': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control', 'maxlength': '20', 'placeholder': 'Phone Number'}
            ),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }