from .models import Wishlist
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from stock.models import Product

@login_required
def view_wishlist(request):
    """View to display the wishlist for the authenticated user."""
    try:
        wishlist = Wishlist.objects.get(user=request.user)
    except Wishlist.DoesNotExist:
        # If the Wishlist doesn't exist for the user, create it
        wishlist = Wishlist.objects.create(user=request.user)
    products = wishlist.products.all()
    return render(request, 'wishlist/view_wishlist.html', {'wishlist': wishlist, 'products': products})

@login_required
def add_to_wishlist(request, product_id):
    """View to add a product to the wishlist."""
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    if product not in wishlist.products.all():
        wishlist.products.add(product)
        messages.success(request, f"{product.name} added to your wishlist.")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")
    return redirect('wishlist:view_wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    """View to remove a product from the wishlist."""
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, f"{product.name} removed from your wishlist.")
    else:
        messages.error(request, f"{product.name} is not in your wishlist.")
    return redirect('wishlist:view_wishlist')

@login_required
def clear_wishlist(request):
    """View to remove all products from the wishlist."""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.clear()
    messages.success(request, "Wishlist cleared successfully.")
    return redirect('wishlist:view_wishlist')