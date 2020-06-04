from django.db import models
from django.utils.translation import ugettext_lazy as _


class BorderPoint(models.Model):
    code = models.CharField(max_length=8)
    tag = models.CharField(max_length=3)
    ukr = models.CharField(max_length=500)
    eng = models.CharField(max_length=500)
    region = models.CharField(max_length=30)
    location = models.CharField(max_length=50)
    index = models.CharField(max_length=5)
    street = models.CharField(max_length=255)

    class Meta:
        verbose_name = _('Пункт пропуску')
        verbose_name_plural = _('Пункти пропуску')
        ordering = ('region',)

    def __str__(self):
        return self.code
