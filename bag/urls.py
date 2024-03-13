from django.urls import path
from . import views

urlpatterns = [
    path('add-to-bag/<int:product_id>/', views.add_to_bag, name='add_to_bag'),
    path('remove-from-bag/<int:product_id>/', views.remove_from_bag, name='remove_from_bag'),
    path('view-bag/', views.view_bag, name='view_bag'),
]
