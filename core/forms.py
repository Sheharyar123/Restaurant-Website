from django import forms
from .models import Restaurant


class RestaurantForm(forms.ModelForm):
    restaurant_license = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"})
    )

    class Meta:
        model = Restaurant
        fields = ["restaurant_name", "restaurant_license"]
