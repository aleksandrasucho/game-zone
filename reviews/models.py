from django.db import models
from django.contrib.auth.models import User
from stock.models import Product
from orders.models import Order
from django.db.models import UniqueConstraint

class Review(models.Model):
    """Review model."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_reviews',
        verbose_name='User',
        help_text='The user who wrote the review.'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Product',
        help_text='The product this review is for.'
    )
    rating = models.PositiveIntegerField(
        default=5,
        choices=[(i, i) for i in range(1, 6)],
        verbose_name='Rating',
        help_text='The rating given by the user (1-5).'
    )
    comment = models.TextField(
        verbose_name='Comment',
        help_text='The review comment left by the user.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        constraints = [
            UniqueConstraint(fields=['product', 'user'], name='unique_product_user_review')
        ]

    def __str__(self):
        return f"Review for {self.product.name} by {self.user.username}"
