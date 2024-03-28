from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from stock.models import Product
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

def add_to_bag(request, product_id):
    if 'bag' not in request.session:
        request.session['bag'] = []

    bag = request.session['bag']

    # Assuming product_id is passed as a parameter
    product = get_object_or_404(Product, pk=product_id)

    # Add the product to the bag
    bag.append(product.id)

    # Save the updated bag in the session
    request.session['bag'] = bag

    # Redirect to the bag page
    return redirect('view_bag')

def remove_from_bag(request, product_id):
    if 'bag' in request.session:
        bag = request.session['bag']

        # Check if the product exists in the bag
        if product_id in bag:
            bag.remove(product_id)
            request.session['bag'] = bag
            return redirect('view_bag')  # Redirect to the bag page after removal

    return HttpResponse("Product not found in the bag.")

def view_bag(request):
    # Check if 'bag' key exists in the session
    bag = request.session.get('bag', [])

    # Retrieve the products from the database based on the product IDs stored in the session
    products = Product.objects.filter(pk__in=bag)

    return render(request, 'bag/bag.html', {'products': products})

def checkout(request):
    # Add your checkout logic here
    return render(request, 'bag/checkout.html')  # Render the checkout page template