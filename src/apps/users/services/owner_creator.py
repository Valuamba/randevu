from typing import Any

from django.utils import timezone
from django.conf import settings

import logging

from apps.utils import get_or_none
from apps.users.models import User, AsyncCodeOperation
from apps.users.managers import CustomUserManager
from apps.mailing.tasks import send_mail
from apps.multilanding.services import MultilandingCreator

from randevu.generator import generate_code

from dateutil.relativedelta import relativedelta


logger = logging.getLogger(__name__)


class OwnerCreator:
    def __init__(self, sub_domain: str, email: str, password: str):
        self.sub_domain = sub_domain
        self.email = email
        self.password = password

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.register(self.sub_domain, self.email, self.password)

    def register(self, sub_domain: str, email: str, password: str):
        manager = CustomUserManager()
        
        user = get_or_none(User, email=email)
        if not user:
            logger.info(f'Create user {email}')
            user = manager.create_user(email=email, password=password)
        else:
            logger.info(f'Update user {email}')
            user.set_password(password)
            user.save()

        code_operation = AsyncCodeOperation.objects.create(
            code=generate_code(),
            status=AsyncCodeOperation.WAITING,
            type=AsyncCodeOperation.REGISTRATION,
            user=user,
            expire_date=timezone.now() + relativedelta(minutes=20)
        )

        MultilandingCreator(sub_domain, user)()
                
        logger.info('Sending verification account mail.')
        # send_mail.delay(
        #         to=email,
        #         template_id=settings.VERIFY_ACCOUNT_TEMPLATE_ID,
        #         ctx={
        #             'code': code_operation.code,
        #         },
        #         disable_antispam=True,
        #     )