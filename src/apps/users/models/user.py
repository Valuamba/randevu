import uuid
from typing import List, Any, Dict

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel
from apps.schedule.models import StaffSchedule

from apps.users.managers import CustomUserManager

from phonenumber_field.modelfields import PhoneNumberField


# class UserQuerySet(models.QuerySet):
#     def for_zone(self, zone: str):
#         return self.filter(company__sub_domain=zone)

#     def for_user(self, user):
#         return self.filter(company=user.company)


# UserManager = models.Manager.from_queryset(UserQuerySet)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedUUIDModel):
    # objects = UserManager()

    OWNER = 1
    ADMIN = 2
    EMPLOYEE = 3
    
    USER_ROLES = [
        (OWNER, "Owner"),
        (ADMIN, "Admin"),
        (EMPLOYEE, "Employee")
    ]
    
    EMPLOYEE_CREATE_ROLES = [
        (ADMIN, "Admin"),
        (EMPLOYEE, "Employee")
    ]
    
    WORKING = 1
    NOT_WORKING = 2
    REMOVED = 3

    EMPLOYEE_CREATE_STATUS = [
        (WORKING, "Working"),
        (NOT_WORKING, "Not working")
    ]

    EMPLOYEE_STATUS = [
        (WORKING, "Working"),
        (NOT_WORKING, "Not working"),
        (REMOVED, "Removed")
    ]
    
    name = models.CharField(verbose_name=_("Full Name"), max_length=150, blank=True)
    email = models.EmailField(verbose_name=_("Email Address"), db_index=True, unique=True, blank=False)
    phone = PhoneNumberField(blank=True, unique=True, null=True)
    image = models.CharField(verbose_name=_("Photo Ref"), max_length=300, blank=True)
    thumb_image = models.CharField(verbose_name=_("Photo Ref 80x80"), max_length=300, blank=True)
    
    is_owner = models.BooleanField(verbose_name=_('Is Owner'), default=False)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    role = models.IntegerField(verbose_name=_("User role"), choices=USER_ROLES)
    status = models.IntegerField(verbose_name=_("Position"), choices=EMPLOYEE_STATUS)
    
    date_joined = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)

    company = models.ForeignKey("multilanding.Multilanding", related_name='employees', on_delete=models.PROTECT, null=True)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.email

    def get_async_operations(self) -> List[Any]:
        return self.operations.filter(expire_date__gt=timezone.now())

    def get_work_slots(self, duration = 0) -> Dict[int, List[int]]:
        free_weekly_slots: Dict[int, List[int]] = {}
        for day in self.weekly_schedule.all():
            if not day.is_day_off:                
                free_weekly_slots[day.week_day] = day.get_work_time_range(duration)    
            else:
                free_weekly_slots[day.week_day] = None

        return free_weekly_slots

    # TOdo: add group by days to fast implemntation
    def get_employee_appointments_by_month(self, year: int, month: int) -> Dict[int, List[set]]:
        appointments = self.appointments.filter(
            day__year=year,
            day__month=month
        )
        appointments_range: Dict[int, List[set]] = {}
        for appointment in appointments:
            day = appointment.day.day
            if day not in appointments_range.keys():
                appointments_range[day] = set()
            appointments_range[day] = appointments_range[day].union(appointment.get_appointment_time_range())
        return appointments_range

    def get_schedule(self) -> List[StaffSchedule]:
        return self.weekly_schedule.all()

    def set_schedule(self):
        from apps.schedule.services import WeeklyScheduleCreator
        WeeklyScheduleCreator(self)()

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    
class AsyncCodeOperation(TimeStampedUUIDModel):
    FAILED = "failed"
    SUCCEED = "succeed"
    WAITING = "waiting"
    CODE_STATUSES = [
        (FAILED, "Failed"),
        (SUCCEED, "Succeed"),
        (WAITING, "Waiting")
    ]
    
    REGISTRATION = "registration"
    PASSWORD_RECOVERY = "password_recovery"
    CODE_TYPES = [
        (REGISTRATION, "Registration"),
        (PASSWORD_RECOVERY, "Password recovery")
    ] 
    
    user = models.ForeignKey(User, related_name='operations', on_delete=models.SET_NULL, null=True)
    code = models.IntegerField()
    status = models.CharField(max_length=20, choices=CODE_STATUSES)
    type = models.CharField(max_length=30, choices=CODE_TYPES)
    expire_date = models.DateTimeField()