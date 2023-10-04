from anymail.message import AnymailMessage
from django.core import mail


AnymailMessage(
            subject='Subject',
            body='Hwhehevbvd',
            to=['mmm.marchuk@mail.ru'],
            connection=self.connection,
            from_email=self.from_email,
            template_id=self.template_id,
            merge_global_data=self.normalized_message_context,
        )
