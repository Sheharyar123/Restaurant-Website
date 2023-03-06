from django.contrib import admin
from .models import Payment, Order, OrderedFood


class PaymentAdmin(admin.ModelAdmin):
    list_display = ["transaction_id", "user", "amount", "payment_choice", "status"]
    list_filter = ["payment_choice", "status"]


class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = [
        "order",
        "payment",
        "user",
        "food_item",
        "quantity",
        "price",
        "amount",
    ]
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "payment_method",
        "first_name",
        "city",
        "country",
        "total",
        "status",
        "order_restaurants",
        "is_ordered",
    ]
    list_editable = [
        "is_ordered",
    ]
    list_filter = ["status", "is_ordered", "city", "state", "country"]
    inlines = [OrderedFoodInline]


class OrderedFoodAdmin(admin.ModelAdmin):
    list_display = ["user", "food_item", "order", "price", "quantity", "amount"]


admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.register(OrderedFood, OrderedFoodAdmin)
