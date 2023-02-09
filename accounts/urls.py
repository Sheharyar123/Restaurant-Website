from django.urls import path
from .views import RegisterUser

app_name = "accounts"
urlpatterns = [
    path("registerUser", RegisterUser.as_view(), name="register_user"),
]
