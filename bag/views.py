from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from stock.models import Product
from django.contrib.auth.decorators import login_required
import decimal

def add_to_bag(request, product_id):
    if 'bag' not in request.session or not isinstance(request.session['bag'], dict):
        request.session['bag'] = {}

    bag = request.session['bag']
    product = get_object_or_404(Product, pk=product_id)

    if str(product_id) not in bag:
        bag[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),  # Convert Decimal to float
            'quantity': 1
        }
        request.session['bag'] = bag
        messages.success(request, f"{product.name} has been added to your bag.")
        return redirect('view_bag')
    else:
        messages.info(request, f"{product.name} is already in your bag.")
        return redirect('product_list')

def remove_from_bag(request, product_id):
    if 'bag' in request.session and isinstance(request.session['bag'], dict):
        bag = request.session['bag']
        if str(product_id) in bag:
            del bag[str(product_id)]
            request.session['bag'] = bag
            return redirect('view_bag')
    return HttpResponse("Product not found in the bag.")

def view_bag(request):
    if 'bag' not in request.session or not isinstance(request.session['bag'], dict):
        request.session['bag'] = {}

    bag = request.session.get('bag', {})
    print(f"Debug: Bag contents - {bag}")  # Debugging line
    product_ids = bag.keys()
    products = Product.objects.filter(pk__in=product_ids)
    total_price = sum(item['price'] * item['quantity'] for item in bag.values())

    return render(request, 'bag/bag.html', {'products': products, 'total_price': total_price})
