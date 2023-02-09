from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import UserRegisterationForm

User = get_user_model()
# Create your views here.
class RegisterUser(View):
    def get(self, request, *args, **kwargs):
        form = UserRegisterationForm()
        context = {"form": form}
        return render(request, "accounts/registerUser.html", context)

    def post(self, request, *args, **kwargs):
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            # user_password = form.cleaned_data["password1"]
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user.set_password(user_password)
            # user.save()
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "Your account has been registered successfully!")
            return redirect("core:index")

        else:
            context = {"form": form}
            return render(request, "accounts/registerUser.html", context)
