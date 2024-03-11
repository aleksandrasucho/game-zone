from django.shortcuts import render
from django.views import View

# Create your views here.

class HomeView(View):
    """View for the home page."""

    def get(self, request):
        """Handle GET requests to display the home page."""
        return render(request, 'home.html')