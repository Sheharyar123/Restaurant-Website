from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegisterationForm, RestaurantForm
from .models import UserProfile

User = get_user_model()
# Create your views here.
class RegisterUserView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in!")
            return redirect("accounts:dashboard")
        else:
            form = UserRegisterationForm()
            context = {"form": form}
            return render(request, "accounts/register_user.html", context)

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


class RegisterRestaurantView(View):
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


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in!")
            return redirect("accounts:customer_dashboard")
        else:
            return render(request, "accounts/login.html")

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user=user)
            messages.success(request, "You have logged into your account successfully!")
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "Invalid login credentials!")
            return redirect("accounts:login")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.info(request, "You are logged out.")
        return redirect("accounts:login")


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == User.CUSTOMER:
            return render(request, "accounts/customer_dashboard.html")
        elif user.role == User.RESTAURANT:
            return render(request, "accounts/restaurant_dashboard.html")
        elif user.role is None and user.is_superuser:
            return redirect("/admin/")
