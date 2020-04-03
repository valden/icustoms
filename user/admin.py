from django.contrib import admin
from .models import User
from django.utils.translation import ugettext_lazy as _


admin.site.register(User)
