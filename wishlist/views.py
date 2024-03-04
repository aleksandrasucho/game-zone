from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from stock.models import Product

@login_required
def view_wishlist(request):
    """View to display user's wishlist."""
    wishlist = request.user.wishlist
    products = wishlist.get_products()
    return render(request, 'wishlist/view_wishlist.html', {'wishlist': wishlist, 'products': products})

@login_required
def add_to_wishlist(request, product_id):
    """View to add a product to the wishlist."""
    # Get the product object or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.user.wishlist
    # Try to add the product to the wishlist
    if wishlist.add_to_wishlist(product):
        # Display success message if added
        messages.success(request, f"{product.name} added to your wishlist.")
    else:
        # Display info message if product already exists in wishlist
        messages.info(request, f"{product.name} is already in your wishlist.")
    return redirect('wishlist:view_wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    """View to remove a product from the wishlist."""
    # Get the product object or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.user.wishlist
    # Try to remove the product from the wishlist
    if wishlist.remove_from_wishlist(product):
        # Display success message if removed
        messages.success(request, f"{product.name} removed from your wishlist.")
    else:
        # Display error message if product is not in wishlist
        messages.error(request, f"{product.name} is not in your wishlist.")
    return redirect('wishlist:view_wishlist')

@login_required
def clear_wishlist(request):
    """View to remove all products from the wishlist."""
    wishlist = request.user.wishlist
    # Clear the wishlist
    wishlist.remove_all_from_wishlist()
    # Display success message
    messages.success(request, "Wishlist cleared successfully.")
    return redirect('wishlist:view_wishlist')