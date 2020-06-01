from django.db import models
from user.models import User, Document, Vehicle
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    MaxLengthValidator,
                                    MinLengthValidator)
import datetime
from num2words import num2words
import math
from itertools import zip_longest
from django.db.models import Sum
from django.http import request


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
        null=True,
        blank=True,
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

    class Meta:
        verbose_name = _('Декларація')
        verbose_name_plural = _('Декларації')
        ordering = ('-update_date',)

    def num_kids_words(self):
        return num2words(self.kids_number, lang='uk')

    def get_goods(self):
        return self.goods.filter(entry=self.pk)

    def num_goods(self):
        return self.goods.filter(entry=self.pk).count()

    def total_empty_rows(self):
        total_goods_rows = 0
        for item in self.get_goods():
            print(item.goods_value)
            goods_name_rows = math.ceil(len(item.goods_name) / 30)
            goods_number_rows = math.ceil(
                len(num2words(int(item.goods_number), lang='uk')) / 12)
            total_goods_rows = total_goods_rows + \
                max(goods_name_rows, goods_number_rows)
        return 15 - total_goods_rows

    def goods_total_number(self):
        return self.goods.filter(entry=self.pk).aggregate(Sum('goods_number'))['goods_number__sum']

    def total_num2words(self):
        numb = self.goods_total_number()
        return num2words(numb, lang='uk')

    def goods_total_value(self):
        return self.goods.filter(entry=self.pk).aggregate(Sum('goods_value'))['goods_value__sum']

    def compare_goods_units(self):
        if len(self.get_goods().values('goods_unit').distinct()) == 1:
            return self.get_goods().values('goods_unit').first()['goods_unit']

    def compare_goods_currencies(self):
        if len(self.get_goods().values('goods_currency').distinct()) == 1:
            return self.get_goods().values('goods_currency').first()['goods_currency']

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

    class Meta:
        verbose_name = _('Товар')
        verbose_name_plural = _('Товари')
        ordering = ('-entry',)

    def numinwords(self):
        return num2words(self.goods_number, lang='uk')

    def goods_rows_number(self):
        name_rows = math.ceil(len(self.goods_name) / 30)
        number_rows = math.ceil(len(self.numinwords()) / 12)
        return max(name_rows, number_rows)

    def split_goods_name(self):
        return [(self.goods_name[i:i + 30])
                for i in range(0, len(self.goods_name), 30)]

    def split_goods_number(self):
        return [(self.numinwords()[i:i + 12])
                for i in range(0, len(self.numinwords()), 12)]

    def zip_goods(self):
        return zip_longest(self.split_goods_name(), self.split_goods_number(), fillvalue='')

    def __str__(self):
        return str(self.entry)
