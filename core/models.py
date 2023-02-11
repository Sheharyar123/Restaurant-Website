from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import UserProfile
from accounts.utils import send_approval_notification

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

    def save(self, *args, **kwargs):
        if self.pk is not None:
            restaurant = Restaurant.objects.get(pk=self.pk)
            if restaurant.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                context = {
                    "user": self.user,
                    "is_approved": self.is_approved,
                    "to_email": self.user.email,
                }
                if self.approved == True:
                    # Send approval notification email
                    mail_subject = "Congratulations! Your restaurant has been approved."
                    send_approval_notification(mail_subject, mail_template, context)
                else:
                    # Send non approval notification email
                    mail_subject = "We're sorry! You are not eligible for publishing your food menu on our marketplace."
                    send_approval_notification(mail_subject, mail_template, context)

        return super(Restaurant, self).save(*args, **kwargs)

    def __str__(self):
        return self.restaurant_name
