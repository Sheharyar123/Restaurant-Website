from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View

from .forms import UserRegisterationForm, RestaurantForm
from .models import UserProfile
from .utils import send_verification_email, send_reset_password_email

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
            mail_subject = "Please activate your account"
            email_template = "accounts/emails/account_email_verification.html"
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(
                request, "We have sent you an email to verify your account!"
            )
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
            # Send verification Mail
            mail_subject = "Please activate your account"
            email_template = "accounts/emails/account_email_verification.html"
            send_verification_email(request, user, mail_subject, email_template)
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


class ActivateView(View):
    def get(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(kwargs.get("uidb64")).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(
            user, token=kwargs.get("token")
        ):
            user.is_active = True
            user.save()
            messages.success(request, "Congratulations! Your account is activated.")
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "Invalid activation link. Please try again")
            return redirect("accounts:dashboard")


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in!")
            return redirect("accounts:dashboard")
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


class ForgotPasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/forgot_password.html")

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            # Send reset password email
            mail_subject = "Please Reset your password"
            email_template = "accounts/emails/password_reset_email.html"
            send_reset_password_email(request, user, mail_subject, email_template)
            messages.success(
                request, "Password reset link has been sent to your email address."
            )
            return redirect("accounts:login")
        else:
            messages.error(request, "Account does not exist!")
            return redirect("accounts:forgot_password")


class ResetPasswordValidateView(View):
    def get(self, request, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(kwargs.get("uidb64")).decode()
            user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(
            user, token=kwargs.get("token")
        ):
            request.session["uid"] = uid
            messages.info(request, "Please reset your password")
            return redirect("accounts:reset_password")
        else:
            messages.error(request, "Reset Password Link expired! Please try again")
            return redirect("accounts:forgot_password")


class ResetPasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "accounts/reset_password.html")

    def post(self, request, *args, **kwargs):
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        # user = User.objects.get(pk=request.session["uid"])
        if password == confirm_password:
            pk = request.session.get("uid")
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password reset successful")
            return redirect("accounts:login")
        else:
            messages.error(request, "Passwords don't match! Please try again!")
            return redirect("accounts:reset_password")


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == User.CUSTOMER:
            return render(request, "accounts/customer_dashboard.html")
        elif user.role == User.RESTAURANT:
            return render(request, "accounts/restaurant_dashboard.html")
        elif user.role is None and user.is_superuser:
            return redirect("/admin/")
