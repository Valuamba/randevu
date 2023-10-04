from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.db.models import Q

# from apps.users.models import User


class CustomUserManager(BaseUserManager):
    def for_employee_viewset(self):
        user = apps.get_model('users.User')
        query = Q(role__in=[user.EMPLOYEE, user.ADMIN]) & ~Q(status=user.REMOVED)

        return self.filter(query)

    def for_zone(self, zone: str):
        User = apps.get_model('users.User')
        query = Q(company__sub_domain=zone) & Q(role__in=[User.EMPLOYEE, User.ADMIN]) & ~Q(status=User.REMOVED)

        return self.filter(query)

    def for_user(self, user):
        User = apps.get_model('users.User')
        query = Q(company=user.company) & Q(role__in=[User.EMPLOYEE, User.ADMIN]) & ~Q(status=User.REMOVED)

        return self.filter(query)
        # return self.filter(company=user.company)

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    def validate_email(self, email):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Base User Account: An email address is required"))

    def create_user(
        self, email, password, **extra_fields
    ):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Base User Account: An email address is required"))

        extra_fields.setdefault("role", apps.get_model('users.User').OWNER)
        extra_fields.setdefault("status", apps.get_model('users.User').WORKING)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_owner", True)

        user = apps.get_model('users.User')(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, password, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superusers must have is_superuser=True"))

        if not password:
            raise ValueError(_("Superusers must have a password"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Admin Account: An email address is required"))

        user = self.create_user(
            email, password, **extra_fields
        )
        user.save(using=self._db)
        return 