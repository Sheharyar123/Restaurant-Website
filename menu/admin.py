from django.contrib import admin
from .models import Category, FoodItem

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category_title", "restaurant", "added_on"]
    prepopulated_fields = {"slug": ("category_title",)}
    list_display_links = ["category_title", "restaurant"]
    search_fields = ["category_title", "restaurant__restaurant_name"]


class FoodItemAdmin(admin.ModelAdmin):
    list_display = [
        "food_title",
        "price",
        "restaurant",
        "category",
        "is_available",
        "added_on",
    ]
    prepopulated_fields = {"slug": ("food_title",)}
    list_display_links = ["food_title", "restaurant", "category"]
    list_filter = [
        "is_available",
    ]
    search_fields = [
        "food_title",
        "restaurant__restaurant_name",
        "category__category_title",
        "price",
    ]
    list_editable = [
        "is_available",
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
