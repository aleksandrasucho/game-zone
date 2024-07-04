from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse 
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm, OrderItemForm
from orders.models import Order, OrderItem
from stock.models import Product, ProductInventory
import json
import stripe
import logging

# Define logger
logger = logging.getLogger(__name__)

@require_POST
def cache_checkout_data(request):
    try:
        client_secret = request.POST.get('client_secret', '')
        pid = client_secret.split('_secret')[0] if client_secret else None
        if pid:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.PaymentIntent.modify(pid, metadata={
                'bag': json.dumps(request.session.get('bag', {})),
                'save_info': request.POST.get('save_info'),
                'username': request.user.username,
            })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be processed right now. Please try again later.')
        logger.error(f"Error caching checkout data: {e}")
        return HttpResponse(content=e, status=400)

@login_required
def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    if 'bag' not in request.session or not isinstance(request.session['bag'], dict):
        request.session['bag'] = {}

    bag = request.session['bag']
    products = Product.objects.filter(pk__in=bag.keys())

    intent = None
    total_price = sum(item['price'] * item['quantity'] for item in bag.values())

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user
            order.total_paid = total_price
            order.save()

            # Create order items
            for product_id, item_data in bag.items():
                product = Product.objects.get(pk=product_id)
                product_inventory = ProductInventory.objects.get(product=product)  # Ensure ProductInventory exists
                order_item = OrderItem.objects.create(
                    order=order,
                    product_inventory=product_inventory,
                    quantity=item_data['quantity'],
                    lineitem_total=item_data['price'] * item_data['quantity']
                )

            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(total_price * 100),
                    currency='gbp',
                    description='Order Payment',
                    metadata={
                        'bag': json.dumps(bag),
                        'order_id': order.id,
                    },
                )
                return redirect(reverse('checkout_success', args=[order.order_number]))
            except stripe.error.CardError as e:
                messages.error(request, 'There was an issue with your card: {}'.format(e))
                return render(request, 'checkout/checkout.html', {'order_form': order_form, 'products': products, 'error': str(e)})
    else:
        order_form = OrderForm()

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),
                currency='gbp',
                metadata={
                    'bag': json.dumps(bag),
                },
            )
        except Exception as e:
            messages.error(request, 'Sorry, we could not process your payment. Please try again later.')
            return redirect('view_bag')

    context = {
        'order_form': order_form,
        'products': products,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret if intent else None,
        'total_price': total_price if 'total_price' in locals() else None,
    }
    return render(request, 'checkout/checkout.html', context)

def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    total_price = order.total_paid

    # Clear the session bag
    if 'bag' in request.session:
        del request.session['bag']
        messages.success(request, 'Your purchase was successful and your bag has been emptied.')

    context = {'order': order, 'total_price': total_price}
    return render(request, 'checkout/checkout_success.html', context)
