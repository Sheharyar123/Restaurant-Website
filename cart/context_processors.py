from menu.models import FoodItem
from .models import Cart, Tax


def get_cart_counter(request):
    cart_count = 0
    try:
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items:
            for cart_item in cart_items:
                cart_count += cart_item.quantity
    except:
        pass
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    subtotal = tax = grand_total = 0
    tax_dict = {}
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        taxes = Tax.objects.filter(is_active=True)
        for cart_item in cart_items:
            food_item = FoodItem.objects.get(pk=cart_item.food_item.id)
            subtotal += food_item.price * cart_item.quantity
        for tax in taxes:
            tax_amount = round((tax.tax_percentage * subtotal) / 100, 2)
            tax_dict.update({tax.tax_type: {str(tax.tax_percentage): tax_amount}})
        tax = sum(x for key in tax_dict.values() for x in key.values())
        grand_total = subtotal + tax
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total, tax_dict=tax_dict)
