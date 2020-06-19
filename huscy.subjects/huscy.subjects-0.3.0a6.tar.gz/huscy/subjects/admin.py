from django.contrib import admin

from huscy.subjects import models


admin.site.register(models.Address)
admin.site.register(models.Contact)
admin.site.register(models.Phone)
admin.site.register(models.Subject)
