from django.contrib import admin
from .models import Cart, Tax


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "food_item", "quantity", "created_on", "updated_on"]
    list_display_links = ["user", "food_item"]


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ["tax_type", "tax_percentage", "is_active"]
    list_editable_fields = [
        "is_active",
    ]
