from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from core.models import Restaurant


class Category(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="categories"
    )
    category_title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified_on", "-added_on"]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def save(self, *args, **kwargs):
        self.slug = (
            self.slug or f"{slugify(self.category_title)}-{self.restaurant.user.id}"
        )
        return super(Category, self).save(*args, **kwargs)

    def clean(self):
        self.category_title = self.category_title.capitalize()

    def get_absolute_url(self):
        return reverse("menu:category_detail", args=[self.slug])

    def __str__(self):
        return self.category_title


class FoodItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="food_items"
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="food_items"
    )
    food_title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="food_items")
    is_available = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified_on", "-added_on"]

    def save(self, *args, **kwargs):
        self.slug = self.slug or f"{slugify(self.food_title)}-{self.restaurant.user.id}"
        return super(FoodItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.food_title
