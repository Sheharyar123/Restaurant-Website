from django.urls import path
from .views import HomePageView, RestaurantProfileView, RestaurantDetailView

app_name = "core"

urlpatterns = [
    path("", HomePageView.as_view(), name="index"),
    path(
        "restaurant/profile/",
        RestaurantProfileView.as_view(),
        name="restaurant_profile",
    ),
    path(
        "restaurant/<slug:restaurant_slug>/",
        RestaurantDetailView.as_view(),
        name="my_restaurant",
    ),
]
