from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductInventory

@receiver(post_save, sender=Product)
def create_product_inventory(sender, instance, created, **kwargs):
    if created:
        ProductInventory.objects.create(product=instance, quantity_available=0)