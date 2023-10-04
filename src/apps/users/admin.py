from django.contrib import admin

from apps.users.models import AsyncCodeOperation



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from apps.users.models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = [
        "pkid",
        "id",
        'phone',
        'image',
        'status',
        'date_joined',
        'company',
        "email",
        'role',
        "name",
        'is_owner',
        "is_staff",
        "is_active",
        'update_at',
        'created_at'
    ]
    list_display_links = ["id", "email"]
    list_filter = [
        "email",
        "name",
        "is_staff",
        "is_active",
    ]
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal Information"),
            {
                "fields": (
                    "name",
                )
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ["email", "name"]



admin.site.register(User, UserAdmin)


class AsyncCodeOperationAdmin(admin.ModelAdmin):
    list_display = [ 'code', 'status', 'type', 'user', 'expire_date', 'created_at', 'update_at']



admin.site.register(AsyncCodeOperation, AsyncCodeOperationAdmin)
