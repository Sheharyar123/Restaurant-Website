from django.contrib.auth import get_user_model
from django.db import models
from menu.models import FoodItem

User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Cart"


class Tax(models.Model):
    tax_type = models.CharField(max_length=50, unique=True)
    tax_percentage = models.DecimalField(
        decimal_places=2, max_digits=4, verbose_name="Tax Percentage (%)"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Taxes"

    def __str__(self):
        return self.tax_type
