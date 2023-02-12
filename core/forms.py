from django import forms
from .models import Restaurant
from accounts.validators import allow_only_images


class RestaurantForm(forms.ModelForm):
    restaurant_license = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_images],
    )

    class Meta:
        model = Restaurant
        fields = ["restaurant_name", "restaurant_license"]
