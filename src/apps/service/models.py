
from tabnanny import verbose
from typing import Dict

from django.apps import apps
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property
from django.conf import settings

from randevu.models import ModelWithLocales

from apps.users.models.user import User
from apps.service.validators import validate_salon_service


class CategoryQuerySet(models.QuerySet):
    def for_zone(self, zone: str):
        return self.filter(company__sub_domain=zone)

    def for_user(self, user):
        return self.filter(company=user.company)


CategoryManager = models.Manager.from_queryset(CategoryQuerySet)


class Category(ModelWithLocales):
    objects = CategoryManager()

    TITLE = "name"
    DESCRIPTION = "description"
    
    LOCALIZED_FIELDS = [
        (TITLE, "Name"),
        (DESCRIPTION, "Description")
    ]

    image = models.CharField(verbose_name=_("Category Photo"), max_length=300, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    company = models.ForeignKey("multilanding.Multilanding", related_name='categories', on_delete=models.PROTECT, null=True)
    
    @property
    def name(self) -> Dict[str, str]:
        return self.get_locale_property(self.TITLE)

    @property
    def description(self) -> Dict[str, str]:
        return self.get_locale_property(self.DESCRIPTION)

    class Meta:
        db_table = 'category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        
    def __str__(self) -> str:
        return self.name[settings.DEFAULT_LANG]
    
    
class ServiceQuerySet(models.QuerySet):
    def for_zone(self, zone: str):
        return self.filter(company__sub_domain=zone)

    def for_user(self, user):
        return self.filter(company=user.company)


ServiceManager = models.Manager.from_queryset(ServiceQuerySet)


class SalonService(ModelWithLocales):
    objects = ServiceManager()

    NAME = "name"
    DESCRIPTION = "description"

    LOCALIZED_FIELDS = [
        (NAME, "Name"),
        (DESCRIPTION, "Description")
    ]

    MALE = 1
    FEMALE = 2
    
    SERVICE_GENDERS = [
        (MALE, 'Male'), 
        (FEMALE, 'Female')
    ]
    
    duration = models.IntegerField(verbose_name=_('Duration'), validators=[validate_salon_service])
    gender = models.IntegerField(verbose_name=_('Gender'), choices=SERVICE_GENDERS)
    is_deleted = models.BooleanField(default=False)

    price = models.FloatField(verbose_name=_('Price'), default=0)
    image = models.CharField(verbose_name=_('Iamge'), max_length=500)

    category = models.ForeignKey(Category, related_name='services', on_delete=models.PROTECT)
    
    employees = models.ManyToManyField('users.User', related_name='services')

    company = models.ForeignKey("multilanding.Multilanding", related_name='services', on_delete=models.PROTECT, null=True)

    # @property
    # def employees(self):
    #     return self.employees.exclude(status=User.REMOVED)

    @property
    def categories(self):
        return self.categories.exclude(is_deleted=True)

    @property
    def name(self) -> Dict[str, str]:
        return self.get_locale_property(self.NAME)

    @property
    def description(self) -> Dict[str, str]:
        return self.get_locale_property(self.DESCRIPTION)
    
    class Meta:
        db_table = 'salon.service'
        verbose_name = _('Salon service')
        verbose_name = _('Salong services')

    def __str__(self) -> str:
        return 'salon'
        return self.name[settings.DEFAULT_LANG]
    
    