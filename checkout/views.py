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
            # Calculate total paid, update other fields as needed
            order.save()

            # Process payment using Stripe
            try:
                # Create a PaymentIntent on the server
                intent = stripe.PaymentIntent.create(
                    amount=order.get_total() * 100,  # Stripe requires amount in cents
                    currency='gbp',  # Use the appropriate currency code
                    description='Order Payment',  # Optional description
                    metadata={'order_id': order.id},  # Optional metadata
                )
            except stripe.error.CardError as e:
                # Display error to the user
                return render(request, 'checkout/checkout.html', {'order_form': order_form, 'products': products, 'error': str(e)})

            # Redirect to success page if payment is successful
            if intent.status == 'succeeded':
                return redirect('checkout_success')

    else:
        order_form = OrderForm()

    return render(request, 'checkout/checkout.html', {'order_form': order_form, 'products': products, 'stripe_public_key': stripe_public_key})
