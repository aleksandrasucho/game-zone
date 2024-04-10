from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from orders.forms import OrderForm
from stock.models import Product
import stripe

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
