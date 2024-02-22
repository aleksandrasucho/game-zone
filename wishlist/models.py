from django.db import models
from stock.models import Product
from profiles.models import User

class Wishlist(models.Model):
    """Model representing a user's wishlist."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        related_name='wishlist'
    )
    
    class Meta:
        """Meta options for the Wishlist model."""
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        """Return a string representation of the wishlist."""
        return f"{self.user}'s Wishlist"

    def add_to_wishlist(self, product):
        """Add a product to the wishlist."""
        if product not in self.products.all():
            self.products.add(product)
            return True
        return False

    def remove_from_wishlist(self, product):
        """Remove a product from the wishlist."""
        if product in self.products.all():
            self.products.remove(product)
            return True
        return False

    def remove_all_from_wishlist(self):
        """Remove all products from the wishlist."""
        self.products.clear()
        return True

    def get_products(self):
        """Return all products in the wishlist."""
        return self.products.all()