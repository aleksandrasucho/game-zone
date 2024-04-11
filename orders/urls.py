from django.urls import path
from .views import (
    UserOrdersView,
    UserOrderDetailsView,
)

app_name = 'orders'

urlpatterns = [
    path('user/orders/', UserOrdersView.as_view(), name='user_order_list'),
    path('user/orders/<slug:order_number>/', UserOrderDetailsView.as_view(), name='user_order_detail'),
]
