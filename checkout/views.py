import json
import stripe

from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
    )
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm
from stock.models import Product
import logging

# Define logger
logger = logging.getLogger(__name__)

@require_POST
def cache_checkout_data(request):
    try:
        print("POST request data:", request.POST)  # Debugging statement
        # Retrieve the PaymentIntent ID from the POST request
        client_secret = request.POST.get('client_secret', '')
        pid = client_secret.split('_secret')[0]
        print("PaymentIntent ID (pid):", pid)  # Debugging statement
        
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
    """
    View to handle checkout process.
    """

    # Retrieve Stripe API keys from Django settings
    stripe_public_key = 'pk_test_51P3N3GP6tR9JlH7YrUVcruhL6O0aqwq2pgcHjY1hs4XapzigC9h5UI8khOBHvBemHRbce7vyp0yL1j7R1KZAjRXV00aeMAq4h6'
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Set the Stripe API key
    stripe.api_key = stripe_secret_key
    
    # Retrieve the bag items from the session
    bag = request.session.get('bag', [])
    
    # Retrieve the products from the database based on the product IDs stored in the session
    products = Product.objects.filter(pk__in=bag)

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            # Calculate total paid based on the sum of product prices
            total_amount = sum(product.price for product in products)
            # Save total amount in the order
            order.total_paid = total_amount
            order.save()

            # Process payment using Stripe
            try:
                # Create a PaymentIntent on the server
                intent = stripe.PaymentIntent.create(
                    amount=int(total_amount * 100),  # Convert total amount to cents
                    currency='gbp',  # Use the appropriate currency code
                    description='Order Payment',  # Optional description
                    metadata={'order_id': order.id},  # Optional metadata
                )
            except stripe.error.CardError as e:
                # Display error to the user
                return render(request, 'checkout/checkout.html', {'order_form': order_form, 'products': products, 'error': str(e)})

            # Redirect to success page if payment is successful
            if intent.status == 'succeeded':
                # Redirect to checkout success page after successful payment
                return render(request, 'checkout_success.html', {'order': order})

    else:
        order_form = OrderForm()

    # Calculate the total price of all products in the bag
    total_price = sum(product.price for product in products)

    return render(request, 'checkout/checkout.html', {'order_form': order_form, 'products': products, 'stripe_public_key': stripe_public_key, 'total_price': total_price})
