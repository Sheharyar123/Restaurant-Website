from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from menu.models import FoodItem
from .context_processors import get_cart_counter, get_cart_amounts
from .models import Cart


class CartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        context = {"cart_items": cart_items}
        return render(request, "cart/cart.html", context)


class AddToCartView(View):
    # Check if user is logged in
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if request is an ajax request
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                try:
                    food_item = FoodItem.objects.get(id=kwargs.get("food_id"))
                    try:
                        user_cart = Cart.objects.get(
                            user=request.user, food_item=food_item
                        )
                        user_cart.quantity += 1
                        user_cart.save()
                        return JsonResponse(
                            {
                                "status": "Success",
                                "message": "Increased the cart quantity",
                                "cart_counter": get_cart_counter(request),
                                "cart_quantity": user_cart.quantity,
                                "cart_amount": get_cart_amounts(request),
                            }
                        )
                    except:
                        new_cart = Cart.objects.create(
                            user=request.user,
                            food_item=food_item,
                            quantity=1,
                        )
                        return JsonResponse(
                            {
                                "status": "Success",
                                "message": "Created new cart",
                                "cart_counter": get_cart_counter(request),
                                "cart_quantity": new_cart.quantity,
                                "cart_amount": get_cart_amounts(request),
                            }
                        )
                except:
                    return JsonResponse(
                        {"status": "Failed", "message": "This food does not exist!"}
                    )
            else:
                return JsonResponse({"status": "Failed", "message": "Invalid request!"})
        else:
            return JsonResponse(
                {"status": "login_required", "message": "Please login to continue"}
            )


class DecreaseCartView(View):
    def get(self, request, *args, **kwargs):
        # Check if user is logged in
        if request.user.is_authenticated:
            # Check if request is an ajax request
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                try:
                    food_item = FoodItem.objects.get(id=kwargs.get("food_id"))
                    try:
                        user_cart = Cart.objects.get(
                            user=request.user, food_item=food_item
                        )
                        if user_cart.quantity > 1:
                            user_cart.quantity -= 1
                            user_cart.save()
                        else:
                            user_cart.delete()
                            user_cart.quantity = 0
                        return JsonResponse(
                            {
                                "status": "Success",
                                "message": "Decreased the cart quantity",
                                "cart_counter": get_cart_counter(request),
                                "cart_quantity": user_cart.quantity,
                                "cart_amount": get_cart_amounts(request),
                            }
                        )
                    except:
                        return JsonResponse(
                            {
                                "status": "Failed",
                                "message": "You do not have this item in your cart!",
                            }
                        )
                except:
                    return JsonResponse(
                        {"status": "Failed", "message": "This food does not exist!"}
                    )
            else:
                return JsonResponse({"status": "Failed", "message": "Invalid request!"})
        else:
            return JsonResponse(
                {"status": "login_required", "message": "Please login to continue"}
            )


class CartItemDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            try:
                cart_item = Cart.objects.get(
                    user=request.user, id=kwargs.get("cart_item_id")
                )
                cart_item.delete()
                return JsonResponse(
                    {
                        "status": "Success",
                        "message": "Cart Item has been deleted",
                        "cart_counter": get_cart_counter(request),
                        "cart_amount": get_cart_amounts(request),
                    }
                )
            except:
                return JsonResponse(
                    {"status": "Failed", "message": "This cart item does not exist!"}
                )
        else:
            return JsonResponse({"status": "Failed", "message": "Invalid request!"})
