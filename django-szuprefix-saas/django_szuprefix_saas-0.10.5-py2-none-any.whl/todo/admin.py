from django.contrib import admin

from . import models


@admin.register(models.Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'name', 'user', 'is_done', 'expiration', 'update_time')
    list_filter = ('is_done', )
    raw_id_fields = ('party', 'user')
    search_fields = ("name",)
    readonly_fields = ('party',)
