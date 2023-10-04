from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.common.models import TimeStampedUUIDModel



class EmailConfiguration(TimeStampedUUIDModel):
    """Configuration is the low-level email backend settings, e.g. email backend class, `mail_from`, or raw backend kwargs
    """
    class BACKEND(models.TextChoices):
        UNSET = '', _('Unset')
        POSTMARK = 'anymail.backends.postmark.EmailBackend', _('Postmark')

    backend = models.CharField(max_length=256, choices=BACKEND.choices, default=BACKEND.UNSET)
    from_email = models.CharField(_('Email sender'), max_length=256, help_text=_('E.g.Info Randevu &lt;info@randevu.beauty&gt;. MUST configure postmark!'))

    backend_options = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = _('Email configuration')
        verbose_name_plural = _('Email configurations')

    def __str__(self) -> str:
        return super().__str__()  # type: ignore
