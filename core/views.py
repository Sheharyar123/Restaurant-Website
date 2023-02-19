from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Prefetch, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from cart.models import Cart
from menu.models import Category, FoodItem
from .forms import RestaurantForm
from .models import Restaurant


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
