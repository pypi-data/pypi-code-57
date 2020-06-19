# from django.contrib import admin
#
# from remo_app.remo.models import Annotation, AnnotationSet, Task, Class, Tool, Tag, License, Dataset, DatasetImage, \
#     Feedback
#
#
# @admin.register(Annotation)
# class AnnotationAdmin(admin.ModelAdmin):
#     list_display = ('image', 'annotation_set', 'updated_at')
#
#
# @admin.register(AnnotationSet)
# class AnnotationSetAdmin(admin.ModelAdmin):
#     list_display = ('name', 'updated_at', 'task', 'model', 'user', 'dataset', 'is_draft')
#
#     def is_draft(self, obj):
#         return False
#
#     is_draft.boolean = False
#
#
# @admin.register(Feedback)
# class FeedbackAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'created_at', 'page_url')
#
#
# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Class)
# class ClassAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(Tool)
# class ToolAdmin(admin.ModelAdmin):
#     pass
#
#
# class DatasetImageInline(admin.TabularInline):
#     model = DatasetImage
#     extra = 5
#
#
# @admin.register(Dataset)
# class DatasetAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'images_count', 'is_archived')
#     inlines = [DatasetImageInline, ]
#
#     def images_count(self, obj):
#         return obj.images.count()
#
#     images_count.allow_tags = True
#     images_count.short_description = 'Images'
#
#
# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#
#
# @admin.register(License)
# class LicenseAdmin(admin.ModelAdmin):
#     pass
