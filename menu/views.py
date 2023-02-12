from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from .forms import CategoryForm
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


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = "menu/category_detail.html"
    context_object_name = "category"

    def get_object(self):
        restaurant = get_restaurant(self.request)
        category = Category.objects.get(
            restaurant=restaurant, slug=self.kwargs.get("category_slug")
        )
        return category


class AddCategoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CategoryForm
        context = {"form": form}
        return render(request, "menu/add_category.html", context)

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.restaurant = get_restaurant(request)
            category.save()
            messages.success(request, "Category was added successfully!")
            return redirect("menu:menu_builder")
        else:
            context = {"form": form}
            return render(request, "menu/add_category.html", context)


class EditCategoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs.get("category_slug"))
        form = CategoryForm(instance=category)
        context = {"form": form, "category": category}
        return render(request, "menu/edit_category.html", context)

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs.get("category_slug"))
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category was updated successfully!")
            return redirect("menu:menu_builder")
        else:
            context = {"form": form}
            return render(request, "menu/add_category.html", context)


class DeleteCategoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(slug=kwargs.get("category_slug"))
        category.delete()
        messages.success(request, "Category was deleted successfully!")
        return redirect("menu:menu_builder")
