from django.urls import path
from .views import (
    RegisterUserView,
    RegisterRestaurantView,
    LoginView,
    LogoutView,
    DashboardView,
)

app_name = "accounts"

urlpatterns = [
    path("registerUser/", RegisterUserView.as_view(), name="register_user"),
    path(
        "registerRestaurant/",
        RegisterRestaurantView.as_view(),
        name="register_restaurant",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
