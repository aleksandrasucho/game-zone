from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, View
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Order, OrderItem
from django.contrib import messages
from .forms import OrderForm, OrderItemForm
from stock.models import ProductInventory
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

# View for listing orders of the logged-in user
class UserOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'user_order_list.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        """Filter orders based on the currently logged-in user."""
        return self.model.objects.filter(user=self.request.user).order_by('-created_at')

# View for displaying details of an order of the logged-in user
class UserOrderDetailsView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'user_order_detail.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        context['order_items'] = order.order_items.all()
        return context

@method_decorator(require_POST, name='dispatch')
class CancelOrderView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        order_number = kwargs.get('order_number')
        order = get_object_or_404(Order, order_number=order_number, user=request.user)

        if order.status == Order.PENDING:
            order.status = Order.CANCELLED
            order.save()

            # Sending email notification
            subject = 'Order Cancellation Notification'
            html_message = render_to_string('order_cancel_email.html', {'order': order, 'user': request.user})
            plain_message = strip_tags(html_message)
            from_email = 'your-email@example.com'
            to_email = [request.user.email]

            send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

            messages.success(request, 'Order has been cancelled successfully.')
        else:
            messages.error(request, 'Order cannot be cancelled.')

        return redirect('orders:user_order_detail', order_number=order.order_number)
