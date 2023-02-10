from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import UserProfile

# Create your models here.

User = get_user_model()


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor")
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="vendor"
    )
    restaurant_name = models.CharField(max_length=100)
    restaurant_license = models.FileField(upload_to="restaurant/licenses")
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified_on", "-created_on"]

    def __str__(self):
        return self.restaurant_name
