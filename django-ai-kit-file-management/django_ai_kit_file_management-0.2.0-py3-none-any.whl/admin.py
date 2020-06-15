from django.contrib import admin

from .models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    exclude = ("size", "format")
    readonly_fields = ("size", "format")
