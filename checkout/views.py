from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm
from stock.models import Product  # Import the Product model

@login_required
def checkout(request):
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
            return redirect('checkout_success')  # Redirect to success page
    else:
        order_form = OrderForm()

    return render(request, 'checkout/checkout.html', {'order_form': order_form, 'products': products})
