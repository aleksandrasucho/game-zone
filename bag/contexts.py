from django.shortcuts import get_object_or_404
from stock.models import Product

def bag_contents(request):
    """Return the contents of the shopping bag."""
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', [])

    if bag:
        for product_id in bag:
            product = get_object_or_404(Product, pk=product_id)
            total += product.price
            product_count += 1
            bag_items.append({
                'product': product,
            })
    
    
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
    }
    return context