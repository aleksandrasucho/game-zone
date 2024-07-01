import uuid
from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.contrib.auth.models import User
from stock.models import Product, ProductInventory
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
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0

        product_count = 0

        for line_item in self.lineitems.all():
            product_count += line_item.quantity

        if product_count >= settings.DISCOUNT_THRESHOLD:
            self.discount = Decimal(
                self.order_total * settings.DISCOUNT_RATE) / 100
        else:
            self.discount = 0

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = settings.STANDARD_DELIVERY_CHARGE
        else:
            self.delivery_cost = 0

        self.grand_total = (
            self.order_total + self.delivery_cost - self.discount
        )
        self.vat = Decimal(self.grand_total * settings.STANDARD_VAT_RATE / 100)
        self.save()


    def _generate_order_number(self):
        """Generate a random, unique order number using UUID"""
        return uuid.uuid4().hex.upper()

    def get_total(self):
        """
        Calculate and return the total amount of the order,
        including any discounts and delivery costs.
        """
        order_items_total = sum(item.lineitem_total for item in self.lineitems.all())
        total_discount = self.discount if hasattr(self, 'discount') else 0
        total_delivery_cost = self.delivery_cost if hasattr(self, 'delivery_cost') else 0
        total_vat = self.vat if hasattr(self, 'vat') else 0

        grand_total = (
            order_items_total + total_delivery_cost - total_discount + total_vat
        )

        return grand_total

class OrderItem(models.Model):
    """Model for OrderItem."""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_inventory.product.name} - {self.quantity}"

class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE,
        related_name='lineitems'
    )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
    )
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.title} on order {self.order.order_number}'
