from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    middle_name = models.CharField(
        _('по батькові'),
        max_length=50,
        null=True,
        blank=True)
    image = models.ImageField(
        _('зображення'),
        upload_to='accounts/images/',
        null=True,
        blank=True)
    residence = CountryField(
        _('резиденство'),
        blank_label=_('Оберіть країну...'),
        blank=True)
    nationality = CountryField(
        _('громадянство'),
        blank_label=_('Оберіть країну...'),
        blank=True)
    birthday = models.DateField(
        _('дата народження'),
        null=True,
        blank=True)
    terms = models.BooleanField(
        _('погодження з умовами'),
        default=False,
        blank=False)

    def __str__(self):
        return self.username
