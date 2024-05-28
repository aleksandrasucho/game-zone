import json
import stripe
import logging

from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm
from orders.models import Order
from stock.models import Product
from bag.contexts import bag_contents

# Define logger
logger = logging.getLogger(__name__)

@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)

@login_required
def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    bag = request.session.get('bag', {})
    products = Product.objects.filter(pk__in=bag)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            total_amount = sum(product.price for product in products)
            order.total_paid = total_amount
            order.save()

            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(total_amount * 100),
                    currency='gbp',
                    description='Order Payment',
                    metadata={'order_id': order.id},
                )
                return redirect(reverse('checkout_success', args=[order.order_number]))
            except stripe.error.CardError as e:
                messages.error(request, 'There was an issue with your card: {}'.format(e))
                return render(request, 'checkout/checkout.html', {'order_form': order_form, 'products': products, 'error': str(e)})
    else:
        order_form = OrderForm()
        total_price = sum(product.price for product in products)
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),
                currency='gbp',
                metadata={'bag': json.dumps(request.session.get('bag', {}))},
            )
        except Exception as e:
            messages.error(request, 'Sorry, we could not process your payment. Please try again later.')
            return redirect('view_bag')

    context = {
        'order_form': order_form,
        'products': products,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        'total_price': total_price,
    }
    return render(request, 'checkout/checkout.html', context)

def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    total_price = order.total_paid  # Assuming total_paid represents the amount paid by the user

    context = {'order': order, 'total_price': total_price}
    return render(request, 'checkout/checkout_success.html', context)

