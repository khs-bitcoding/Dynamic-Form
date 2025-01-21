from django.contrib import admin
from app import models as AM

# Register your models here.
admin.site.register(AM.FieldList)
admin.site.register(AM.Form)
admin.site.register(AM.FormFields)
admin.site.register(AM.FormAnswer)
