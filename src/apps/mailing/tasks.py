from typing import Union

import requests
from anymail.exceptions import AnymailRequestsAPIError

from randevu.celery import celery
from apps.mailing.owl import Owl


@celery.task(
    autoretry_for=[AnymailRequestsAPIError],
    retry_kwargs={
        'max_retries': 10,
        'countdown': 5,
    },
    acks_late=True,
)
def send_mail(to: str, template_id: str, subject: Union[str, None] = '', ctx: Union[dict, None] = None, disable_antispam: Union[bool, None] = False):
    Owl(
        to=to,
        template_id=template_id,
        subject=subject,
        ctx=ctx,
        disable_antispam=disable_antispam,
    )()