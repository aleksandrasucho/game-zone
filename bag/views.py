from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from stock.models import Product
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse

def add_to_bag(request, product_id):
    if 'bag' not in request.session:
        request.session['bag'] = []

    bag = request.session['bag']

    # Assuming product_id is passed as a parameter
    product = get_object_or_404(Product, pk=product_id)

    # Check if the product is already in the bag
    if product.id not in bag:
        # Add the product to the bag if it's not already there
        bag.append(product.id)
        # Save the updated bag in the session
        request.session['bag'] = bag
        # Inform the user that the product has been added to the bag
        messages.success(request, f"{product.name} has been added to your bag.")
        # Redirect to the bag page
        return redirect('view_bag')
    else:
        # Inform the user that the product is already in the bag
        messages.info(request, f"{product.name} is already in your bag.")
        return redirect('product_list')  # Redirect to a different page or stay on the same page

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
    bag = request.session.get('bag', [])
    products = Product.objects.filter(pk__in=bag)

    # Calculate the total price of all products in the bag
    total_price = sum(product.price for product in products)

    return render(request, 'bag/bag.html', {'products': products, 'total_price': total_price})


def checkout(request):
    # Add your checkout logic here
    return render(request, 'bag/checkout.html')  # Render the checkout page template