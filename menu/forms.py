from django import forms
from accounts.validators import allow_only_images
from .models import Category, FoodItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["category_title", "description"]


class FoodItemForm(forms.ModelForm):
    image = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-primary w-100"}),
        validators=[allow_only_images],
    )

    class Meta:
        model = FoodItem
        fields = [
            "category",
            "food_title",
            "price",
            "description",
            "image",
            "is_available",
        ]
