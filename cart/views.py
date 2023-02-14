from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from menu.models import FoodItem
from django.http import JsonResponse
from .context_processors import get_cart_counter
from .models import Cart


@login_required(login_url="account:login")
def add_to_cart(request, food_id):
    # Check if request is an ajax request
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        try:
            food_item = FoodItem.objects.get(id=food_id)
            try:
                user_cart = Cart.objects.get(user=request.user, food_item=food_item)
                user_cart.quantity += 1
                user_cart.save()
                return JsonResponse(
                    {
                        "status": "Success",
                        "message": "Increased the cart quantity",
                        "cart_counter": get_cart_counter(request),
                        "cart_quantity": user_cart.quantity,
                    }
                )
            except:
                new_cart = Cart.objects.create(
                    user=request.user, food_item=food_item, quantity=1
                )
                return JsonResponse(
                    {
                        "status": "Success",
                        "message": "Created new cart",
                        "cart_counter": get_cart_counter(request),
                        "cart_quantity": new_cart.quantity,
                    }
                )
        except:
            return JsonResponse(
                {"status": "Failed", "message": "This food does not exist!"}
            )
    else:
        return JsonResponse({"status": "Failed", "message": "Invalid request!"})
