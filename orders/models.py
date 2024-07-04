import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.models import User
from stock.models import ProductInventory
from decimal import Decimal

class Order(models.Model):
    """Model for Order."""
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    COMPLETED = 'Completed'
    REFUNDED = 'Refunded'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (COMPLETED, 'Completed'),
        (REFUNDED, 'Refunded'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=100, blank=True)
    address_1 = models.CharField(max_length=250)
    address_2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    order_number = models.CharField(max_length=32, unique=True, editable=False)
    billing_status = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.order_number)

    def save(self, *args, **kwargs):
        """Override the save method to set the order number."""
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
        
    def update_total(self):
        """
        Update grand total for the order.
        """
        order_items_total = self.order_items.aggregate(
            total=Sum('lineitem_total')
        )['total'] or Decimal('0.00')

        self.order_total = order_items_total

        if self.order_total >= Decimal(settings.DISCOUNT_THRESHOLD):
            self.discount = self.order_total * Decimal(settings.DISCOUNT_RATE) / Decimal('100')
        else:
            self.discount = Decimal('0.00')

        if self.order_total < Decimal(settings.FREE_DELIVERY_THRESHOLD):
            self.delivery_cost = Decimal(settings.STANDARD_DELIVERY_CHARGE)
        else:
            self.delivery_cost = Decimal('0.00')

        self.grand_total = (
            self.order_total + self.delivery_cost - self.discount
        )

        self.vat = self.grand_total * Decimal(settings.STANDARD_VAT_RATE) / Decimal('100')

        self.save()

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def get_total(self):
        """
        Calculate and return the total amount of the order,
        including any discounts and delivery costs.
        """
        return self.grand_total if hasattr(self, 'grand_total') else Decimal('0.00')


class OrderItem(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    lineitem_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00')
    )

    def save(self, *args, **kwargs):
        self.lineitem_total = self.product_inventory.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_inventory.product.name} - {self.quantity}"
