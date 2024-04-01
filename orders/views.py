from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from stock.models import Product

# View for listing orders
class OrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        """Filter orders based on the logged-in user."""
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

# View for displaying order details
class OrderDetailsView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

# View for editing an order
class EditOrderView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'edit_order.html'
    success_url = reverse_lazy('order_list')

# View for deleting an order
class DeleteOrderView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'delete_order.html'
    success_url = reverse_lazy('order_list')

# View for editing an order item
class EditOrderItemView(LoginRequiredMixin, UpdateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'edit_order_item.html'
    success_url = reverse_lazy('order_list')

# View for deleting an order item
class DeleteOrderItemView(LoginRequiredMixin, DeleteView):
    model = OrderItem
    template_name = 'delete_order_item.html'
    success_url = reverse_lazy('order_list')

# View for confirming payment
def payment_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Logic for confirming payment and sending confirmation email
    return render(request, 'payment_confirmation.html', {'order': order})

# View for listing orders of the logged-in user
class UserOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'user_order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        """Filter orders based on the currently logged-in user."""
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

# View for displaying details of an order of the logged-in user
class UserOrderDetailsView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'user_order_detail.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'