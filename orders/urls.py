from django.urls import path
from .views import UserOrdersView, UserOrderDetailsView, CancelOrderView

app_name = 'orders'

urlpatterns = [
    path('user/orders/', UserOrdersView.as_view(), name='user_order_list'),
    path('user/orders/<slug:order_number>/', UserOrderDetailsView.as_view(), name='user_order_detail'),
    path('user/orders/<slug:order_number>/cancel/', CancelOrderView.as_view(), name='cancel_order'),
]