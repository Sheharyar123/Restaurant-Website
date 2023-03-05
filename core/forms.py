from django import forms
from django.contrib.auth import get_user_model
from .models import Restaurant, OpeningHour
from accounts.validators import allow_only_images
from orders.models import Order

User = get_user_model()


class RestaurantForm(forms.ModelForm):
    restaurant_license = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_images],
    )

    class Meta:
        model = Restaurant
        fields = ["restaurant_name", "restaurant_license"]


class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ["day", "from_hour", "to_hour", "is_closed"]


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_no"]


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "phone_no",
            "email",
            "address",
            "city",
            "state",
            "country",
            "pin_code",
        ]
