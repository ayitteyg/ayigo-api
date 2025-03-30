from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin, ExportMixin, ImportMixin

# Register your models here.

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
   pass
