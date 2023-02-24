from django.contrib.auth import get_user_model
from django import forms

from .models import UserProfile
from .validators import allow_only_images

User = get_user_model()


class UserRegisterationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]

    def clean(self):
        cleaned_data = super(UserRegisterationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords Don't Match!")


class UserProfileForm(forms.ModelForm):
    profile_pic = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_images],
        required=False,
    )
    cover_photo = forms.FileField(
        widget=forms.FileInput(attrs={"class": "btn btn-info"}),
        validators=[allow_only_images],
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = [
            "profile_pic",
            "cover_photo",
            "address",
            "country",
            "state",
            "city",
            "pin_code",
            "latitude",
            "longitude",
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field in ["latitude", "longitude"]:
                self.fields[field].widget.attrs.update({"readonly": "readonly"})
