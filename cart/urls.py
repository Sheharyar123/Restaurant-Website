from django.urls import path
from .views import CartView, CartItemDeleteView, AddToCartView, DecreaseCartView

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="user_cart"),
    path("<int:food_id>/add/", AddToCartView.as_view(), name="add_to_cart"),
    path("<int:food_id>/remove/", DecreaseCartView.as_view(), name="decrease_cart"),
    path(
        "delete/<int:cart_item_id>/",
        CartItemDeleteView.as_view(),
        name="delete_cart_item",
    ),
]
