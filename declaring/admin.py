from django.contrib import admin
from .models import Entry, Goods
from django.utils.translation import ugettext_lazy as _


admin.site.register(Entry)
admin.site.register(Goods)
