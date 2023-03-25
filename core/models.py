from datetime import time, date, datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from accounts.models import UserProfile
from accounts.utils import send_approval_notification

User = get_user_model()


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor")
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="vendor"
    )
    restaurant_name = models.CharField(max_length=100, unique=True)
    restaurant_slug = models.SlugField(unique=True, max_length=100)
    restaurant_license = models.ImageField(upload_to="restaurant/licenses")
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-modified_on", "-created_on"]

    def save(self, *args, **kwargs):
        self.restaurant_slug = self.restaurant_slug or slugify(self.restaurant_name)
        if self.pk is not None:
            restaurant = Restaurant.objects.get(pk=self.pk)
            if restaurant.is_approved != self.is_approved:
                mail_template = "accounts/emails/admin_approval_email.html"
                context = {
                    "user": self.user,
                    "is_approved": self.is_approved,
                    "to_email": self.user.email,
                }
                if self.is_approved == True:
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

    def is_open(self):
        # Check current day's opening hours.
        today_date = date.today()
        today = today_date.isoweekday()
        print(today)

        current_opening_hours = OpeningHour.objects.filter(restaurant=self, day=today)
        print(current_opening_hours)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        is_open = None
        for i in current_opening_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour, "%I:%M %p").time())
                print(start)
                end = str(datetime.strptime(i.to_hour, "%I:%M %p").time())
                print(end)
                if current_time > start and current_time < end:
                    is_open = True
                    print(is_open)
                    break
                else:
                    is_open = False
        return is_open

    def get_absolute_url(self):
        return reverse(
            "core:restaurant_detail", kwargs={"restaurant_slug": self.restaurant_slug}
        )


DAYS = (
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
)

HOURS = [
    (time(h, m).strftime("%I:%M %p"), time(h, m).strftime("%I:%M %p"))
    for h in range(0, 24)
    for m in (0, 30)
]


class OpeningHour(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="opening_hours"
    )
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOURS, max_length=20, blank=True)
    to_hour = models.CharField(choices=HOURS, max_length=20, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ("day", "-from_hour")
        unique_together = ("restaurant", "day", "from_hour", "to_hour")

    def __str__(self):
        return f"{self.restaurant.restaurant_name}'s opening hour"
