from django.contrib import admin
from .models import User, Document, Vehicle
from django.utils.translation import ugettext_lazy as _


admin.site.register(User)
admin.site.register(Document)
admin.site.register(Vehicle)
