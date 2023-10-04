from typing import Any

from django.utils import timezone
from django.conf import settings

import logging
from apps.users.exceptions import UserException

from apps.utils import get_or_none
from apps.users.models import User, AsyncCodeOperation
from apps.users.managers import CustomUserManager
from apps.mailing.tasks import send_mail

from randevu.generator import generate_code

from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


class RecoveryCodeSender:
    def __init__(self, email: str) -> None:
        self.email = email

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.send(self.email)

    def send(self, email: str):
        logger.info('Send recover code.')
    
        user = get_or_none(User, email=email)
        
        if not user:
            raise UserException(text=f"User with {email} doesn't exist.", x_code='x006')
        
        if user.is_active == False:
            raise UserException(text="User should be activated.", x_code='x005')
        
        if user.is_staff == True:
            raise UserException(text="User cannot be staff.")
        
        code_operation = AsyncCodeOperation.objects.create(
            code=generate_code(),
            status=AsyncCodeOperation.WAITING,
            type=AsyncCodeOperation.PASSWORD_RECOVERY,
            user=user,
            expire_date=timezone.now() + relativedelta(minutes=20)
        )
        
        logger.info('Sending recover code.')
        # send_mail.delay(
        #         to=email,
        #         template_id=settings.PASSWORD_RESET_TEMPLATE_ID,
        #         ctx={
        #             'email': email,
        #             'code': code_operation.code,
        #             'product_name': settings.RANDEVU_DOMAIN
        #         },
        #         disable_antispam=True,
        #     )