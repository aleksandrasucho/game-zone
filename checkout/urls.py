from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<str:order_number>/', views.checkout_success, name='checkout_success'),
    path('checkout/checkout/cache_checkout_data/', views.cache_checkout_data, name='cache_checkout_data'),
]
