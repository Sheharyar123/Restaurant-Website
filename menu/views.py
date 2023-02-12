from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView
from .models import Category
from .utils import get_restaurant


class MenuBuilderView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "menu/menu_builder.html"
    context_object_name = "category_list"

    def get_queryset(self):
        restaurant = get_restaurant(self.request)
        category_list = Category.objects.filter(restaurant=restaurant)
        return category_list
