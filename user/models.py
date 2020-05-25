from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    MaxLengthValidator,
                                    MinLengthValidator)
import datetime
from django.http import request


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
        if self.get_full_name():
            return self.get_full_name()
        else:
            return self.username


class Document(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='document')
    doc_name = models.CharField(
        _('назва'),
        max_length=250,
        null=True,
        blank=False)
    doc_number = models.CharField(
        _('номер'),
        max_length=250,
        null=True,
        blank=False)
    doc_date = models.DateField(
        _('дата'),
        null=True,
        blank=False)

    class Meta:
        verbose_name = _("Документ")
        verbose_name_plural = _("Документи")

    def __str__(self):
        return " - ".join([self.user.get_full_name(), self.doc_name])


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Vehicle(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicle')
    auto_name = models.CharField(
        _('марка'),
        max_length=250,
        null=True,
        blank=False)
    auto_year = models.PositiveIntegerField(
        _('рік випуску'),
        default=current_year(),
        validators=[MinValueValidator(1950), max_value_current_year],
        null=True,
        blank=False)
    auto_engine = models.PositiveIntegerField(
        _("об'єм двигуна"),
        default=1600,
        validators=[MinValueValidator(50), MaxValueValidator(9999)],
        null=True,
        blank=False)
    auto_vin = models.CharField(
        _('кузов №'),
        max_length=16,
        validators=[MinLengthValidator(16), MaxLengthValidator(16)],
        null=True,
        blank=False)

    class Meta:
        verbose_name = _("Транспортний засіб")
        verbose_name_plural = _("Транспортні засоби")

    def __str__(self):
        return " - ".join([self.user.get_full_name(), self.auto_name])
