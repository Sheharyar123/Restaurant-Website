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
