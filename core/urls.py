from django.urls import path
from .views import (
    HomePageView,
    SearchView,
    OpeningHoursView,
    AddOpeningHourView,
    RemoveOpeningHourView,
    RestaurantListView,
    RestaurantProfileView,
    RestaurantDetailView,
)

app_name = "core"

urlpatterns = [
    path("", HomePageView.as_view(), name="index"),
    path("search/", SearchView.as_view(), name="search"),
    path("marketplace/", RestaurantListView.as_view(), name="restaurant_list"),
    path("opening_hours/", OpeningHoursView.as_view(), name="opening_hours"),
    path("opening_hours/add", AddOpeningHourView.as_view(), name="add_opening_hour"),
    path(
        "opening_hours/remove/<int:hour_id>/",
        RemoveOpeningHourView.as_view(),
        name="remove_opening_hour",
    ),
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
