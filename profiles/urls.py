from django.urls import path
from .views import (
    ProfileView, EditUserProfileView,
    AddressesView, EditAddressView, DeleteAddressView,
    ChangePrimaryAddressView, DeleteProfileView
)

app_name = 'profiles'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditUserProfileView.as_view(), name='edit_profile'),
    path('addresses/', AddressesView.as_view(), name='addresses'),
    path('edit_address/<int:address_id>/', EditAddressView.as_view(), name='edit_address'),
    path('delete_address/<int:address_id>/', DeleteAddressView.as_view(), name='delete_address'),
    path('change_primary_address/<int:address_id>/', ChangePrimaryAddressView.as_view(), name='change_primary_address'),
    path('delete_profile/', DeleteProfileView.as_view(), name='delete_profile'),
]