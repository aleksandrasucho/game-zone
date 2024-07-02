from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from orders.models import OrderItem  # Adjust import to use OrderItem

@receiver(post_save, sender=OrderItem)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on order item update/create
    """
    instance.order.update_total()

@receiver(post_delete, sender=OrderItem)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on order item delete
    """
    instance.order.update_total()