from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm
from stock.models import Product

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
