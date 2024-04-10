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
        # Retrieve the PaymentIntent ID from the POST request
        client_secret = request.POST.get('client_secret', '')
        pid = client_secret.split('_secret')[0]
        
        # Log the received PaymentIntent ID
        logger.info('Received PaymentIntent ID: %s', pid)
        
        # Set the Stripe API key
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Modify the PaymentIntent metadata to cache checkout data
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': str(request.user),  # Convert user object to string
        })
        
        # Return a success response
        return HttpResponse(status=200)
    except Exception as e:
        # Log any exceptions that occur
        logger.exception('Error occurred while caching checkout data: %s', e)
        
        # Handle exceptions
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        return HttpResponse(content=str(e), status=400)


@login_required
def checkout(request):
    stripe_public_key = 'pk_test_51P3N3GP6tR9JlH7YrUVcruhL6O0aqwq2pgcHjY1hs4XapzigC9h5UI8khOBHvBemHRbce7vyp0yL1j7R1KZAjRXV00aeMAq4h6'
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    stripe.api_key = stripe_secret_key
    
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
                logger.info('Payment intent created: %s', intent)
            except stripe.error.CardError as e:
                logger.error('Card error occurred: %s', str(e))
                return render(request, 'checkout/checkout.html', {'order_form': order_form, 'products': products, 'error': str(e)})

            if intent.status == 'succeeded':
                logger.info('Payment succeeded for order: %s', order.order_number)
                return redirect(reverse('checkout_success', args=[order.order_number]))
            else:
                logger.warning("Payment intent status: %s", intent.status)
    else:
        order_form = OrderForm()

    total_price = sum(product.price for product in products)
    
    context = {
        'order_form': order_form,
        'products': products,
        'stripe_public_key': stripe_public_key,
        'total_price': total_price,
        'client_secret': 'test client secret',  # Adjust this as needed
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    logger.info('Checkout success for order: %s', order_number)

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
