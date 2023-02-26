import simplejson as json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from cart.context_processors import get_cart_amounts
from cart.models import Cart
from core.forms import CheckoutForm
from .models import Order
from .utils import generate_order_number


class PlaceOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items.count() < 1:
            return redirect("core:restaurant_list")
        return render(request, "orders/place_order.html")

    def post(self, request, *args, **kwargs):
        subtotal = get_cart_amounts(request).get("subtotal")
        total_tax = get_cart_amounts(request).get("tax")
        grand_total = get_cart_amounts(request).get("grand_total")
        tax_data = get_cart_amounts(request).get("tax_dict")
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order()
            order.user = request.user
            order.first_name = form.cleaned_data["first_name"]
            order.last_name = form.cleaned_data["last_name"]
            order.phone_no = form.cleaned_data["phone_no"]
            order.email = request.user.email
            order.address = form.cleaned_data["address"]
            order.city = form.cleaned_data["city"]
            order.state = form.cleaned_data["state"]
            order.country = form.cleaned_data["country"]
            order.pin_code = form.cleaned_data["pin_code"]
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST.get("payment_method")
            order.save()
            order.order_number = generate_order_number(order.id)
            order.save()
            return redirect("orders:place_order")
        else:
            pass
