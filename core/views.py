from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from menu.models import Category, FoodItem
from .forms import RestaurantForm
from .models import Restaurant


class HomePageView(ListView):
    model = Restaurant
    template_name = "core/index.html"
    context_object_name = "top_restaurants"

    def get_queryset(self):
        top_restaurants = Restaurant.objects.filter(
            is_approved=True, user__is_active=True
        )[:8]
        return top_restaurants


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
        return context
