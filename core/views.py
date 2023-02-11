from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from .models import Restaurant


class HomePageView(TemplateView):
    template_name = "core/index.html"


class RestaurantDetailView(LoginRequiredMixin, DetailView):
    model = Restaurant
    template_name = "core/restaurant_detail.html"
    context_object_name = "restaurant"

    def get_object(self):
        queryset = Restaurant.objects.get(
            restaurant_slug=self.kwargs.get("restaurant_slug"), user=self.request.user
        )
        return queryset
