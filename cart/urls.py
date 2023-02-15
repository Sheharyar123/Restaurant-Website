from django.urls import path
from .views import add_to_cart, decrease_cart

app_name = "cart"

urlpatterns = [
    path("<int:food_id>/add/", add_to_cart, name="add_to_cart"),
    path("<int:food_id>/remove/", decrease_cart, name="decrease_cart"),
]
