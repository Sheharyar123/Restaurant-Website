from accounts.models import UserProfile
from core.models import Restaurant

from django.conf import settings


def get_restaurant(request):
    try:
        restaurant = Restaurant.objects.get(user=request.user)
    except:
        restaurant = None
    return dict(restaurant=restaurant)


def get_user_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        user_profile = None
    return dict(user_profile=user_profile)


def get_google_api_key(request):
    return dict(GOOGLE_API_KEY=settings.GOOGLE_API_KEY)


def get_paypal_client_id(request):
    return dict(PAYPAL_CLIENT_ID=settings.PAYPAL_CLIENT_ID)
