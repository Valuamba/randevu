from apps.common.models import TimeStampedUUIDModel
from django.db import models


class EmailLogEntry(TimeStampedUUIDModel):
    email = models.CharField(max_length=255, null=False)
    template_id = models.CharField(max_length=255, null=False)

    class Meta:
        index_together = ['email', 'template_id']
        unique_together = ['email', 'template_id']
