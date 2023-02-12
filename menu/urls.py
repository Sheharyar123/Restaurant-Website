from django.urls import path
from .views import MenuBuilderView

app_name = "menu"

urlpatterns = [
    path("builder/", MenuBuilderView.as_view(), name="category_list"),
]
