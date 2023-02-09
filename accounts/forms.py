from django.contrib.auth import get_user_model
from django import forms

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
