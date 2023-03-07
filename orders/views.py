from django.http import JsonResponse
import simplejson as json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import View
from accounts.models import UserProfile
from accounts.utils import send_approval_notification
from cart.context_processors import get_cart_amounts
from cart.models import Cart, Tax
from core.forms import CheckoutForm
from core.models import Restaurant
from menu.models import FoodItem
from .models import Order, Payment, OrderedFood
from .utils import generate_order_number


class PlaceOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items.count() < 1:
            return redirect("core:restaurant_list")
        return render(request, "orders/place_order.html")

    def post(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        restaurant_ids = []
        for item in cart_items:
            res_id = item.food_item.restaurant.id
            if res_id not in restaurant_ids:
                restaurant_ids.append(res_id)

        taxes = Tax.objects.filter(is_active=True)
        subtotal_dict = {}
        total_data = {}
        subtotal = 0
        for item in cart_items:
            food_item = FoodItem.objects.get(
                id=item.food_item.id, restaurant__id__in=restaurant_ids
            )
            if food_item.id in subtotal_dict:
                subtotal = subtotal_dict[food_item.id]
                subtotal += food_item.price * item.quantity
            else:
                subtotal = food_item.price * item.quantity

            subtotal_dict[food_item.id] = subtotal
            tax_dict = {}
            for tax in taxes:
                tax_type = tax.tax_type
                tax_percentage = tax.tax_percentage
                tax_amount = round((tax_percentage * subtotal) / 100, 2)
                tax_dict.update({tax_type: {str(tax_percentage): str(tax_amount)}})
            total_data.update({food_item.restaurant.id: {str(subtotal): str(tax_dict)}})
            print(total_data)

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
            order.email = form.cleaned_data["email"]
            order.address = form.cleaned_data["address"]
            order.city = form.cleaned_data["city"]
            order.state = form.cleaned_data["state"]
            order.country = form.cleaned_data["country"]
            order.pin_code = form.cleaned_data["pin_code"]
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax
            order.payment_method = request.POST.get("payment_method")
            order.save()
            order.restaurants.add(*restaurant_ids)
            order.order_number = generate_order_number(order.id)
            order.save()
            context = {"order": order, "cart_items": cart_items}
            return render(request, "orders/place_order.html", context)
        else:
            pass


class ReceivePaymentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            transaction_id = request.POST.get("transaction_id")
            status = request.POST.get("status")
            payment_choice = request.POST.get("payment_choice")
            order_number = request.POST.get("order_number")
            amount = get_cart_amounts(request).get("grand_total")
            order = Order.objects.get(order_number=order_number, user=request.user)
            payment = Payment.objects.create(
                user=request.user,
                transaction_id=transaction_id,
                status=status,
                payment_choice=payment_choice,
                amount=amount,
            )
            order.payment = payment
            order.is_ordered = True
            order.save()

            # Move Cart items to Ordered Food model
            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                ordered_food = OrderedFood()
                ordered_food.order = order
                ordered_food.payment = payment
                ordered_food.user = request.user
                ordered_food.food_item = item.food_item
                ordered_food.quantity = item.quantity
                ordered_food.price = item.food_item.price
                ordered_food.amount = item.food_item.price * item.quantity
                ordered_food.save()

            # Send email to user
            mail_subject = "Thank you for your order"
            mail_template = "orders/order_confirmation.html"
            context = {
                "order": order,
                "to_email": order.email,
                "payment": payment,
            }
            send_approval_notification(mail_subject, mail_template, context)

            # Send email to vendors
            mail_subject = "You received a new order"
            mail_template = "orders/order_received.html"
            to_emails = []
            for item in cart_items:
                email = item.food_item.restaurant.user.email
                if email not in to_emails:
                    to_emails.append(email)
            context = {
                "to_email": to_emails,
                "order": order,
            }

            send_approval_notification(mail_subject, mail_template, context)

            # Clear cart
            cart_items.delete()

            return JsonResponse(
                {
                    "status": "success",
                    "order_number": order.order_number,
                    "transaction_id": payment.transaction_id,
                }
            )
        else:
            return JsonResponse({"status": "failed"})


class OrderCompleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order_number = request.GET.get("order_number")
        transaction_id = request.GET.get("trans_id")
        try:
            order = Order.objects.get(
                order_number=order_number,
                payment__transaction_id=transaction_id,
                is_ordered=True,
            )
            ordered_food = OrderedFood.objects.filter(order=order, user=request.user)
            subtotal = 0
            for item in ordered_food:
                subtotal += item.amount
            tax_data = json.loads(order.tax_data)
            context = {
                "order": order,
                "ordered_food": ordered_food,
                "subtotal": subtotal,
                "tax_data": tax_data,
            }
        except:
            return redirect("core:restaurant_list")
        return render(request, "orders/order_complete.html", context)


class CustomerOrdersView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user, is_ordered=True)
        context = {"orders": orders}
        return render(request, "orders/customer_orders.html", context)


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(
                order_number=kwargs.get("order_number"), is_ordered=True
            )
            ordered_food = OrderedFood.objects.filter(order=order)
            subtotal = 0
            for item in ordered_food:
                subtotal += item.quantity * item.price
            tax_data = json.loads(order.tax_data)
            context = {
                "order": order,
                "ordered_food": ordered_food,
                "subtotal": subtotal,
                "tax_data": tax_data,
            }
            return render(request, "orders/order_detail.html", context)
        except:
            return redirect("accounts:dashboard")


class RestaurantOrderDetailView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            restaurant = Restaurant.objects.get(user=request.user)
            order = Order.objects.get(
                order_number=kwargs.get("order_number"), is_ordered=True
            )
            ordered_food = OrderedFood.objects.filter(order=order)
            context = {
                "order": order,
                "ordered_food": ordered_food,
                "restaurant": restaurant,
                "subtotal": order.get_total_by_restaurant["subtotal"],
                "tax_data": order.get_total_by_restaurant["tax_data"],
                "total": order.get_total_by_restaurant["grand_total"],
            }
            return render(request, "orders/restaurant_order_detail.html", context)
        except:
            return redirect("accounts:dashboard")
