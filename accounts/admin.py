from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# For language translations
from django.utils.translation import gettext_lazy as _

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


admin.site.register(User, UserAdmin)
