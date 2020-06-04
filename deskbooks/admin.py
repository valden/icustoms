from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import BorderPoint


@admin.register(BorderPoint)
class BorderPointAdmin(ImportExportModelAdmin):
    list_display = ['id', 'region', 'code', 'ukr',
                    'location', 'index', 'street']
