from django.urls import path
from .views import RegisterUser, RegisterRestaurant

app_name = "accounts"

urlpatterns = [
    path("registerUser/", RegisterUser.as_view(), name="register_user"),
    path(
        "registerRestaurant/", RegisterRestaurant.as_view(), name="register_restaurant"
    ),
]
