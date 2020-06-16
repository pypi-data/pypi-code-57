from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'title', 'category', 'link', 'user', 'target_user_tags', 'is_active')
    list_filter = ('is_force', 'is_active', 'is_sent')
    raw_id_fields = ('party', 'user')
    readonly_fields = ('target_user_count', 'read_user_count')
    search_fields = ("title",)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'title', 'receiver', 'sender', 'task', 'is_force')
    list_filter = ('is_force', 'is_active', 'is_read')
    raw_id_fields = ('party', 'receiver', 'sender', 'task')
    search_fields = ("title",)
