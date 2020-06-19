from django.contrib import admin
from djangopost.models import CategoryModel
from djangopost.models import ArticleModel
from djangopost.modeladmins import CategoryModelAdmin
from djangopost.modeladmins import ArticleModelAdmin


# Register your models here.
admin.site.register(CategoryModel, CategoryModelAdmin)
admin.site.register(ArticleModel, ArticleModelAdmin)