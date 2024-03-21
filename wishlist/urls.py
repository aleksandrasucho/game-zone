# urls.py in your wishlist app
from django.urls import path

from . import views

app_name = 'wishlist'

urlpatterns = [
    path('view/', views.view_wishlist, name='view_wishlist'),
    path('add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('clear/', views.clear_wishlist, name='clear_wishlist'),
]