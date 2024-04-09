from django import template

register = template.Library()

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity=1):  # Set default quantity to 1
    return price * quantity