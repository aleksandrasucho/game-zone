from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Wishlist
from stock.models import Product

@login_required
def view_wishlist(request):
    """View to display the wishlist for the authenticated user."""
    try:
        # Attempt to get the Wishlist object for the current user
        wishlist = Wishlist.objects.get(user=request.user)
    except Wishlist.DoesNotExist:
        # If the Wishlist doesn't exist for the user, create it
        wishlist = Wishlist.objects.create(user=request.user)
    
    # Get all products in the wishlist
    products = wishlist.products.all()
    
    # Render the wishlist template with the wishlist and products
    return render(request, 'wishlist/view_wishlist.html', {'wishlist': wishlist, 'products': products})

@login_required
def add_to_wishlist(request, product_id):
    """View to add a product to the wishlist."""
    # Get the product object or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create the Wishlist object for the current user
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    # Add the product to the wishlist if it's not already present
    if product not in wishlist.products.all():
        wishlist.products.add(product)
        message = f"{product.name} added to your wishlist."
        success = True
    else:
        message = f"{product.name} is already in your wishlist."
        success = False
    
    # Display message and return JSON response
    messages.success(request, message)
    return JsonResponse({'success': success, 'message': message})

@login_required
def remove_from_wishlist(request, product_id):
    """View to remove a product from the wishlist."""
    # Get the product object or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create the Wishlist object for the current user
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    # Remove the product from the wishlist if it's present
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        message = f"{product.name} removed from your wishlist."
        success = True
    else:
        message = f"{product.name} is not in your wishlist."
        success = False
    
    # Display message and return JSON response
    messages.success(request, message)
    return JsonResponse({'success': success, 'message': message})

@login_required
def clear_wishlist(request):
    """View to remove all products from the wishlist."""
    # Get or create the Wishlist object for the current user
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    # Clear all products from the wishlist
    wishlist.products.clear()
    
    # Display success message
    messages.success(request, "Wishlist cleared successfully.")
    
    # Return JSON response indicating success
    return JsonResponse({'success': True, 'message': 'Wishlist cleared successfully.'})
