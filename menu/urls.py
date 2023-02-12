from django.urls import path
from .views import (
    MenuBuilderView,
    CategoryDetailView,
    AddCategoryView,
    EditCategoryView,
    DeleteCategoryView,
)

app_name = "menu"

urlpatterns = [
    path("builder/", MenuBuilderView.as_view(), name="menu_builder"),
    path("category/add/", AddCategoryView.as_view(), name="add_category"),
    path(
        "category/<category_slug>/",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "category/<category_slug>/edit/",
        EditCategoryView.as_view(),
        name="edit_category",
    ),
    path(
        "category/<category_slug>/delete/",
        DeleteCategoryView.as_view(),
        name="delete_category",
    ),
]
