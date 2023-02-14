from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def add_to_cart(request, food__item_slug):
    return HttpResponse("Testing")
