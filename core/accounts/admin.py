from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["id", "email"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": ("is_staff", "is_superuser", "is_active")}),
        (_("Important Dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active",'is_superuser'),
            },
        ),
    )
    readonly_fields=['last_login']
