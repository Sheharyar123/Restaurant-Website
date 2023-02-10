from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import UserRegisterationForm, RestaurantForm
from .models import UserProfile

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
            return render(request, "accounts/register_user.html", context)


class RegisterRestaurant(View):
    def get(self, request, *args, **kwargs):
        form = UserRegisterationForm
        restaurant_form = RestaurantForm
        context = {"form": form, "restaurant_form": restaurant_form}
        return render(request, "accounts/register_restaurant.html", context)

    def post(self, request, *args, **kwargs):
        form = UserRegisterationForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid() and restaurant_form.is_valid():
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
            user.role = User.RESTAURANT
            user.save()
            user_profile = UserProfile.objects.get(user=user)
            restaurant = restaurant_form.save(commit=False)
            restaurant.user = user
            restaurant.restaurant_name = restaurant_form.cleaned_data["restaurant_name"]
            restaurant.user_profile = user_profile
            restaurant.save()
            messages.success(
                request,
                "Your account has been registered sucessfully! Please wait for the approval",
            )
            return redirect("accounts:register_restaurant")
        else:
            context = {"form": form, "restaurant_form": restaurant_form}
            return render(request, "accounts/register_restaurant.html", context)
