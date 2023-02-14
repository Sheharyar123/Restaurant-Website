from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "food_item", "quantity", "created_on", "updated_on"]
    list_display_links = ["user", "food_item"]


admin.site.register(Cart, CartAdmin)
