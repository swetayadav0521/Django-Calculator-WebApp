from django.db import models
from django.utils import timezone

class History(models.Model):
    result = models.TextField()
    creation_date_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'History'

    def __str__(self):
        return str(self.pk)