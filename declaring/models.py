from django.db import models
from user.models import User, Document, Vehicle
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    MaxLengthValidator,
                                    MinLengthValidator)
import datetime


class Entry(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='entry')
    create_date = models.DateTimeField(
        _('дата створення'),
        auto_now_add=True)
    update_date = models.DateTimeField(
        _('дата створення'),
        auto_now=True)
    direction = models.CharField(
        _('напрям переміщення'),
        max_length=10,
        choices=(
            ('0', _("в'їзд")),
            ('1', _("виїзд"))),
        default=None,
        null=True,
        blank=False)
    passport = models.ForeignKey(
        Document,
        on_delete=models.DO_NOTHING,
        related_name='doc')
    departure = CountryField(
        _('країна відправлення'),
        blank_label=_('Оберіть країну...'),
        blank=True)
    arrival = CountryField(
        _('країна призначення'),
        blank_label=_('Оберіть країну...'),
        blank=True)
    kids_number = models.PositiveIntegerField(
        _('кількість'),
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        null=True,
        blank=True)
    accamp_number = models.PositiveIntegerField(
        _('кількість'),
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        null=True,
        blank=True)
    nonaccamp_number = models.PositiveIntegerField(
        _('кількість'),
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        null=True,
        blank=True)
    cargo_number = models.PositiveIntegerField(
        _('кількість'),
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        null=True,
        blank=True)
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.DO_NOTHING,
        related_name='auto')
    purpose = models.CharField(
        _('мета переміщення'),
        max_length=10,
        choices=(
            ('0', _("тимчасове ввезення")),
            ('1', _("транзит")),
            ('2', _("зворотне вивезення"))),
        default=None,
        null=True,
        blank=True)
    limited = models.CharField(
        max_length=10,
        choices=(
            ('1', _("так")),
            ('0', _("ні")),
        ),
        default=None,
        null=True,
        blank=False)

    def __str__(self):
        return " - ".join([self.user.get_full_name(), str(self.update_date)])


class Goods(models.Model):
    entry = models.ForeignKey(
        Entry,
        on_delete=models.CASCADE,
        related_name='goods')
    goods_name = models.CharField(
        _('найменування'),
        max_length=1000,
        null=True,
        blank=True)
    goods_number = models.PositiveIntegerField(
        _('кількість'),
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        null=True,
        blank=True)
    goods_unit = models.CharField(
        _('одиниця'),
        max_length=10,
        choices=(
            ('0', _("кг")),
            ('1', _("л")),
            ('2', _("шт"))),
        default=None,
        null=True,
        blank=True)
    goods_value = models.PositiveIntegerField(
        _('вартість'),
        default=None,
        validators=[MinValueValidator(0), MaxValueValidator(100000)],
        null=True,
        blank=True)
    goods_currency = models.CharField(
        _('валюта'),
        max_length=10,
        choices=(
            ('0', _("грн.")),
            ('1', _("євро"))),
        default=None,
        null=True,
        blank=True)

    def __str__(self):
        return str(self.entry)
