from django.contrib import admin
from djangocontact.models import EmailModel
from djangocontact.modeladmins import EmailModelAdmin


# Register your models here.
admin.site.register(EmailModel, EmailModelAdmin)