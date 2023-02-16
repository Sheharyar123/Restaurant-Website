from menu.models import FoodItem
from .models import Cart


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
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items:
            for cart_item in cart_items:
                food_item = FoodItem.objects.get(pk=cart_item.food_item.id)
                subtotal += food_item.price * cart_item.quantity
            grand_total = subtotal + tax
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)
