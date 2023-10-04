from apps.schedule.models import StaffBreak, StaffSchedule
from apps.users.models import User, AsyncCodeOperation

from typing import List

from randevu.test.factory import register
from randevu.generator import generate_code

from dateutil.relativedelta import relativedelta

from django.utils import timezone


@register
def multilanding(self, sub_domain):
    multilanding_domain = self.mixer.blend('multilanding.MultilandingDomain', sub_domain=sub_domain)
    
    multilanding = self.mixer.blend('multilanding.Multilanding')
    multilanding.domain = multilanding_domain
    multilanding.sub_domain = sub_domain
    multilanding.save()

    return multilanding


@register
def admin(self, is_active = True, **kwargs):
    owner = self.owner(sub_domain='admindom' ,is_active=True)
    admin = self.mixer.blend('users.User', is_owner=True, is_active=is_active, role=User.ADMIN, \
        status=User.WORKING, company=owner.company, **kwargs    
    )

    return admin


@register
def employee(self, is_active = True, **kwargs):
    owner = self.owner(sub_domain='admindom' ,is_active=True)
    employee = self.mixer.blend('users.User', is_owner=True, is_active=is_active, role=User.EMPLOYEE, \
        status=User.WORKING, company=owner.company, **kwargs    
    )

    return employee


@register
def async_operation(self, user, code, type = AsyncCodeOperation.REGISTRATION, status=AsyncCodeOperation.WAITING):
    code = generate_code() if not code else code
    async_operation = self.mixer.blend('users.AsyncCodeOperation', code=code, status=status, type=type,
            expire_date=timezone.now() + relativedelta(minutes=20)
        )

    async_operation.user = user
    async_operation.save()


@register
def owner(self, sub_domain: str = None, code = None, multilanding = None, is_active = False, **kwargs):
    if not multilanding:
        multilanding = self.multilanding(sub_domain)

    password = kwargs.pop('password', None)

    owner = self.mixer.blend('users.User', is_owner=True, is_active=is_active, role=User.OWNER, \
        status=User.WORKING, company=multilanding, **kwargs   
    )
    
    if password:
        owner.set_password(password)
        owner.save()

    if not is_active:
        self.async_operation(owner, code)

    return owner