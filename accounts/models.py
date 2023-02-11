from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class BaseUserManager(UserManager):
    def create_user(self, email, first_name, last_name, username, password=None):
        if not email:
            raise ValueError("User must have an email address")

        if not username:
            raise ValueError("User must have an username")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, password):
        super_user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
        )
        super_user.is_active = True
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save()
        return super_user


class User(AbstractBaseUser, PermissionsMixin):
    RESTAURANT = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (RESTAURANT, "Restaurant"),
        (CUSTOMER, "Customer"),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=50, null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = BaseUserManager()
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]
    USERNAME_FIELD = "email"

    class Meta:
        ordering = ["-updated_on", "-created_on"]

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(
        upload_to="users/profile_pics", null=True, blank=True
    )
    cover_photo = models.ImageField(
        upload_to="users/cover_photos", null=True, blank=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-modified_on", "-created_on"]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s profile"

    def user_email(self):
        return self.user.email

    def user_first_name(self):
        return self.user.first_name

    def user_last_name(self):
        return self.user.last_name
