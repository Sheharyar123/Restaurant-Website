from django.db import models
from django.contrib.auth import get_user_model
from menu.models import FoodItem

User = get_user_model()


class Payment(models.Model):
    PAYMENT_CHOICES = (
        ("Paypal", "Paypal"),
        ("Stripe", "Stripe"),
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="payments"
    )
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_choice = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id


class Order(models.Model):
    STATUS = (
        ("New", "New"),
        ("Accepted", "Accepted"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    )

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, related_name="orders"
    )
    order_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=50)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    tax_data = models.JSONField(
        blank=True,
        help_text="Data format: {'tax_type':{'tax_percentage':'tax_amount'}}",
        null=True,
    )
    total_data = models.JSONField(blank=True, null=True)
    total_tax = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    status = models.CharField(choices=STATUS, max_length=20, default="New")
    is_ordered = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number


class OrderedFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_items")
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    food_item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE, related_name="order_items"
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True
    )
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_item.food_title
