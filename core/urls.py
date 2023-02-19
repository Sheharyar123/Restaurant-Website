from django.urls import path
from .views import (
    HomePageView,
    SearchView,
    RestaurantListView,
    RestaurantProfileView,
    RestaurantDetailView,
)

app_name = "core"

urlpatterns = [
    path("", HomePageView.as_view(), name="index"),
    path("search/", SearchView.as_view(), name="search"),
    path("marketplace/", RestaurantListView.as_view(), name="restaurant_list"),
    path(
        "restaurant/profile/",
        RestaurantProfileView.as_view(),
        name="restaurant_profile",
    ),
    path(
        "restaurant/<restaurant_slug>/",
        RestaurantDetailView.as_view(),
        name="restaurant_detail",
    ),
]
