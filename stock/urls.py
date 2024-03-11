from django.urls import path
from .views import CategoryListView, CategoryDetailView, ProductListView, ProductDetailView

urlpatterns = [
    # URL patterns for categories
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),

    # URL patterns for products
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]