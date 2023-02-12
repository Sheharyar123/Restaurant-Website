from core.models import Restaurant


def get_restaurant(request):
    try:
        restaurant = Restaurant.objects.get(user=request.user)
    except:
        restaurant = None
    return restaurant
