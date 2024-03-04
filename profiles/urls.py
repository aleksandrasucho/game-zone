from django.urls import path
from .views import (
    ProfileView, EditUserProfileView, ResetAvatarView, EditAvatarAjaxView,
    AddressesView, AddAddressView, EditAddressView, DeleteAddressView,
    ChangePrimaryAddressView, DeleteProfileView
)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit_profile/', EditUserProfileView.as_view(), name='edit_profile'),
    path('reset_avatar/', ResetAvatarView.as_view(), name='reset_avatar'),
    path('edit_avatar_ajax/', EditAvatarAjaxView.as_view(), name='edit_avatar_ajax'),
    path('addresses/', AddressesView.as_view(), name='addresses'),
    path('add_address/', AddAddressView.as_view(), name='add_address'),
    path('edit_address/<int:address_id>/', EditAddressView.as_view(), name='edit_address'),
    path('delete_address/<int:address_id>/', DeleteAddressView.as_view(), name='delete_address'),
    path('change_primary_address/<int:address_id>/', ChangePrimaryAddressView.as_view(), name='change_primary_address'),
    path('delete_profile/', DeleteProfileView.as_view(), name='delete_profile'),
]