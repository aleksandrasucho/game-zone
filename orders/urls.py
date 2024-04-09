from django.urls import path
from .views import (
    EditOrderView,
    DeleteOrderView,
    EditOrderItemView,
    DeleteOrderItemView,
    payment_confirmation,
    UserOrdersView,
    UserOrderDetailsView,
)

app_name = 'orders'

urlpatterns = [
    path('orders/<int:pk>/edit/', EditOrderView.as_view(), name='edit_order'),
    path('orders/<int:pk>/delete/', DeleteOrderView.as_view(), name='delete_order'),
    path('orders/items/<int:pk>/edit/', EditOrderItemView.as_view(), name='edit_order_item'),
    path('orders/items/<int:pk>/delete/', DeleteOrderItemView.as_view(), name='delete_order_item'),
    path('orders/<int:order_id>/payment_confirmation/', payment_confirmation, name='payment_confirmation'),
    path('user/orders/', UserOrdersView.as_view(), name='user_order_list'),
    path('user/orders/<slug:order_number>/', UserOrderDetailsView.as_view(), name='user_order_detail'),
]
