from django.shortcuts import render
from django.views import View
from stock.models import Product

class HomeView(View):
    """View for the home page."""

    def get(self, request):
        """Handle GET requests to display the home page."""
        best_sellers = Product.objects.filter(is_best_seller=True)
        return render(request, 'home.html', {'best_sellers': best_sellers})