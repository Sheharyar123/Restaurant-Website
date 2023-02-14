from django.contrib import admin

from .models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["restaurant_name", "user", "is_approved", "created_on"]
    list_display_links = ["restaurant_name", "user"]
    prepopulated_fields = {"restaurant_slug": ("restaurant_name",)}
    list_editable = [
        "is_approved",
    ]


admin.site.register(Restaurant, RestaurantAdmin)
# admin.site.register(Cart, CartAdmin)
