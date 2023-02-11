from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# For language translations
from django.utils.translation import gettext_lazy as _
from .models import UserProfile

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_filter = ("role", "first_name", "last_name", "username")
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "phone_no",
        "created_on",
        "is_active",
        "is_staff",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal Details"),
            {"fields": ("role", "first_name", "last_name", "username", "phone_no")},
        ),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important Dates"), {"fields": ("last_login", "created_on", "updated_on")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "username",
                    "phone_no",
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    readonly_fields = ("last_login", "created_on", "updated_on")


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user_email",
        "user_first_name",
        "user_last_name",
        "country",
        "state",
        "city",
        "active",
    )
    list_filter = ("country", "city", "state")
    list_editable = [
        "active",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
