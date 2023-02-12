from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, DetailView

from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .forms import RestaurantForm
from .models import Restaurant


class HomePageView(TemplateView):
    template_name = "core/index.html"


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


class RestaurantDetailView(LoginRequiredMixin, DetailView):
    model = Restaurant
    template_name = "core/restaurant_detail.html"
    context_object_name = "restaurant"

    def get_object(self):
        queryset = Restaurant.objects.get(
            restaurant_slug=self.kwargs.get("restaurant_slug"), user=self.request.user
        )
        return queryset
