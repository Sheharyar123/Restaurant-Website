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
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save()
        return super_user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICE = (
        (1, "Restaurant"),
        (2, "Customer"),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    phone_no = models.CharField(max_length=50, null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = BaseUserManager()
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]
    USERNAME_FIELD = "email"

    class Meta:
        ordering = ["-updated_on", "-created_on"]

    def __str__(self):
        return self.email
