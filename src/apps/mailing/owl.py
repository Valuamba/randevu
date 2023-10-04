from pprint import pprint
from typing import Optional, Union
from anymail.message import AnymailMessage
from dataclasses import dataclass
from django.conf import settings
from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend
from django.utils.functional import cached_property

from apps.mailing import helpers
from apps.mailing.models import EmailConfiguration, EmailLogEntry


@dataclass
class Owl:
    """Deliver messages [from Hogwarts] to the particular end-user
    """
    to: str
    template_id: str
    subject: Union[str, None] = ''
    ctx: Union[dict, None] = None
    disable_antispam: Union[bool, None] = False

    def __call__(self) -> None:
        if not settings.EMAIL_ENABLED:
            return

        if self.is_sent_already and not self.disable_antispam:
            return
        
        self.msg.send()
        status = self.msg.anymail_status
        print(status.__dict__)

        self.write_email_log()

    def write_email_log(self) -> None:
        EmailLogEntry.objects.update_or_create(
            email=self.to,
            template_id=self.template_id,
        )

    @cached_property
    def msg(self) -> AnymailMessage:
        return AnymailMessage(
            subject=self.subject,
            body='',
            to=[self.to],
            connection=self.connection,
            from_email=self.from_email,
            template_id=self.template_id,
            merge_global_data=self.normalized_message_context,
        )

    @property
    def connection(self) -> BaseEmailBackend:
        return mail.get_connection(
            fail_silently=False,
            backend=self.backend_name,
            **self.backend_options,
        )

    @property
    def normalized_message_context(self) -> dict:
        if self.ctx is None:
            return {}

        return helpers.normalize_email_context(self.ctx)

    @property
    def is_sent_already(self) -> bool:
        return EmailLogEntry.objects.filter(email=self.to, template_id=self.template_id).exists()

    @cached_property
    def configuration(self) -> Union[EmailConfiguration, None]:
        """
        Configuration works only in production mode to avoid confusing the developer when settings custom email backend
        """
        if not settings.DEBUG:
            return None
            # return get_configuration(recipient=self.to)

    @cached_property
    def backend_name(self) -> str:
        if self.configuration is None or self.configuration.backend == EmailConfiguration.BACKEND.UNSET:
            return settings.EMAIL_BACKEND

        return self.configuration.backend

    @cached_property
    def backend_options(self) -> dict:
        if self.configuration is not None:
            return self.configuration.backend_options

        return {}

    @cached_property
    def from_email(self) -> str:
        if self.configuration is not None:
            return self.configuration.from_email

        return settings.DEFAULT_FROM_EMAIL
