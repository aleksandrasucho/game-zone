from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm

class OrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter orders based on user
        return queryset.filter(user=self.request.user)

class OrderDetailsView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

class EditOrderView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'edit_order.html'
    success_url = reverse_lazy('order_list')

class DeleteOrderView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'delete_order.html'
    success_url = reverse_lazy('order_list')

class EditOrderItemView(LoginRequiredMixin, UpdateView):
    model = OrderItem
    form_class = OrderItemForm
    template_name = 'edit_order_item.html'
    success_url = reverse_lazy('order_list')

class DeleteOrderItemView(LoginRequiredMixin, DeleteView):
    model = OrderItem
    template_name = 'delete_order_item.html'
    success_url = reverse_lazy('order_list')

def payment_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Logic for confirming payment and sending confirmation email
    return render(request, 'payment_confirmation.html', {'order': order})

class UserOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'user_order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter orders based on currently logged-in user
        return queryset.filter(user=self.request.user)

class UserOrderDetailsView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'user_order_detail.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'