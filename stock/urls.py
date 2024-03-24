from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    # URL patterns for products
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]