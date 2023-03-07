from datetime import date
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db import IntegrityError
from django.db.models import Prefetch, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from cart.models import Cart
from menu.models import Category, FoodItem
from menu.utils import get_restaurant
from orders.models import Order
from .forms import RestaurantForm, OpeningHourForm, UserInfoForm, CheckoutForm
from .models import Restaurant, OpeningHour


def get_or_set_current_location(request):
    if "lat" in request.session:
        lat = request.session["lat"]
        lng = request.session["lng"]
        return lat, lng
    elif "lat" in request.GET:
        lat = request.GET.get("lat")
        lng = request.GET.get("lng")
        request.session["lat"] = lat
        request.session["lng"] = lng
        return lat, lng
    else:
        return None


class HomePageView(ListView):
    model = Restaurant
    template_name = "core/index.html"
    context_object_name = "restaurant_list"

    def get_queryset(self):
        if get_or_set_current_location(self.request) is not None:
            latitude, longitude = get_or_set_current_location(self.request)
            pnt = GEOSGeometry(f"POINT({longitude} {latitude})", srid=4326)
            restaurant_list = (
                Restaurant.objects.filter(
                    user_profile__location__distance_lte=(pnt, D(km=1000)),
                    is_approved=True,
                    user__is_active=True,
                )
                .annotate(distance=Distance("user_profile__location", pnt))
                .order_by("distance")
            )[:8]

            for restaurant in restaurant_list:
                restaurant.kms = round(restaurant.distance.km, 1)
        else:
            restaurant_list = Restaurant.objects.filter(
                is_approved=True, user__is_active=True
            )[:8]
        return restaurant_list


class RestaurantListView(ListView):
    model = Restaurant
    template_name = "core/restaurant_list.html"
    context_object_name = "restaurant_list"

    def get_queryset(self):
        restaurant_list = Restaurant.objects.filter(
            is_approved=True, user__is_active=True
        )[:8]
        return restaurant_list


class RestaurantProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        restaurant = Restaurant.objects.get(user_profile=user_profile)

        context = {
            "user_profile": user_profile,
            "restaurant": restaurant,
            "form": UserProfileForm(instance=user_profile),
            "r_form": RestaurantForm(instance=restaurant),
        }

        return render(request, "core/restaurant_profile.html", context)

    def post(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        restaurant = Restaurant.objects.get(user_profile=user_profile)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        r_form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid() and r_form.is_valid():
            form.save()
            r_form.save()
            messages.success(request, "Your profile was updated successfully!")
            return redirect("core:restaurant_profile")
        else:
            messages.error(request, "There was a problem updating")
            context = {
                "form": form,
                "r_form": r_form,
                "user_profile": user_profile,
                "restaurant": restaurant,
            }
            return render(request, "core/restaurant_profile.html", context)


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "core/restaurant_detail.html"
    context_object_name = "restaurant"

    def get_object(self):
        restaurant = get_object_or_404(
            Restaurant, restaurant_slug=self.kwargs.get("restaurant_slug")
        )
        return restaurant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(
            restaurant=self.get_object()
        ).prefetch_related(
            Prefetch("food_items", queryset=FoodItem.objects.filter(is_available=True))
        )
        context["opening_hours"] = OpeningHour.objects.filter(
            restaurant=self.get_object()
        )
        today_date = date.today()
        today = today_date.isoweekday()
        context["current_opening_hours"] = OpeningHour.objects.filter(
            restaurant=self.get_object(), day=today
        )

        try:
            context["cart_items"] = Cart.objects.filter(
                user=self.request.user,
            )
        except:
            context["cart_items"] = []
        return context


class SearchView(View):
    def get(self, request, *args, **kwargs):
        if "address" not in request.GET:
            return redirect("core:restaurant_list")
        else:
            keyword = request.GET.get("keyword")
            user_address = request.GET.get("address")
            latitude = request.GET.get("lat")
            longitude = request.GET.get("lng")
            radius = request.GET.get("radius")

            food_items = FoodItem.objects.filter(
                food_title__icontains=keyword, is_available=True
            )
            restaurants_ids = food_items.values_list("restaurant", flat=True)
            restaurant_list = Restaurant.objects.filter(
                Q(id__in=restaurants_ids)
                | Q(
                    restaurant_name__icontains=keyword,
                    is_approved=True,
                    user__is_active=True,
                )
            )
            if latitude and longitude and radius:
                pnt = GEOSGeometry(f"POINT({longitude} {latitude})", srid=4326)
                restaurant_list = (
                    Restaurant.objects.filter(
                        Q(id__in=restaurants_ids)
                        | Q(
                            restaurant_name__icontains=keyword,
                            is_approved=True,
                            user__is_active=True,
                        ),
                        user_profile__location__distance_lte=(pnt, D(km=radius)),
                    )
                    .annotate(distance=Distance("user_profile__location", pnt))
                    .order_by("distance")
                )

                for restaurant in restaurant_list:
                    restaurant.kms = round(restaurant.distance.km, 1)

            context = {"restaurant_list": restaurant_list, "user_address": user_address}
            return render(request, "core/restaurant_list.html", context)


class OpeningHoursView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        opening_hours = OpeningHour.objects.filter(restaurant=get_restaurant(request))
        form = OpeningHourForm
        context = {"form": form, "opening_hours": opening_hours}
        return render(request, "core/opening_hours.html", context)


class AddOpeningHourView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            day = request.POST.get("day")
            from_hour = request.POST.get("from_hour")
            to_hour = request.POST.get("to_hour")
            is_closed = request.POST.get("is_closed")
            try:
                opening_hour = OpeningHour.objects.create(
                    restaurant=get_restaurant(request),
                    day=day,
                    from_hour=from_hour,
                    to_hour=to_hour,
                    is_closed=is_closed,
                )
                if opening_hour:
                    day = OpeningHour.objects.get(id=opening_hour.id)
                    if day.is_closed:
                        return JsonResponse(
                            {
                                "status": "Success",
                                "id": opening_hour.id,
                                "day": day.get_day_display(),
                                "is_closed": "Closed",
                            }
                        )
                    else:
                        return JsonResponse(
                            {
                                "status": "Success",
                                "id": opening_hour.id,
                                "day": day.get_day_display(),
                                "from_hour": day.from_hour,
                                "to_hour": day.to_hour,
                            }
                        )
            except IntegrityError as e:
                return JsonResponse(
                    {
                        "status": "Failed",
                        "message": f"{from_hour} to {to_hour} already exists for this day!",
                    }
                )
        else:
            HttpResponse("Invalid Request")


class RemoveOpeningHourView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            hour_id = self.kwargs.get("hour_id")
            hour = get_object_or_404(OpeningHour, id=hour_id)
            hour.delete()
            return JsonResponse({"status": "Success", "id": hour_id})


class CustomerProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = UserInfoForm(instance=request.user)
        up_form = UserProfileForm(instance=user_profile)
        context = {"form": form, "up_form": up_form, "user_profile": user_profile}
        return render(request, "core/customer_profile.html", context)

    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(UserProfile, user=request.user)
        form = UserInfoForm(request.POST, instance=request.user)
        up_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid() and up_form.is_valid():
            form.save()
            up_form.save()
            messages.success(request, "Your profile was updated successfully!")
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "There was a problem updating your profile")
            context = {"form": form, "up_form": up_form, "user_profile": user_profile}
            return render(request, "core/customer_profile.html", context)


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items.count() < 1:
            return redirect("core:restaurant_list")
        user_profile = UserProfile.objects.get(user=request.user)

        default_values = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "email": request.user.email,
            "address": user_profile.address,
            "phone_no": request.user.phone_no,
            "city": user_profile.city,
            "state": user_profile.state,
            "country": user_profile.country,
            "pin_code": user_profile.pin_code,
        }
        form = CheckoutForm(initial=default_values)
        context = {"form": form, "cart_items": cart_items}
        return render(request, "core/checkout.html", context)


class RestaurantOrdersView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        restaurant = Restaurant.objects.get(user=request.user)
        orders = Order.objects.filter(restaurants__in=[restaurant.id], is_ordered=True)
        context = {"orders": orders}
        return render(request, "core/restaurant_orders.html", context)
