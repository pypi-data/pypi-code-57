from django.contrib import admin

from . import models


@admin.register(models.Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'party', 'is_active', 'begin_time', 'end_time')
    raw_id_fields = ('party', 'user')
    search_fields = ("title",)
    readonly_fields = ('party',)


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'user', 'survey')
    raw_id_fields = ('party', 'user', 'survey')
    readonly_fields = ('party',)
