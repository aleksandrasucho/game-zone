from django.shortcuts import render
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    # Add checkout logic here
    return render(request, 'checkout/checkout.html')