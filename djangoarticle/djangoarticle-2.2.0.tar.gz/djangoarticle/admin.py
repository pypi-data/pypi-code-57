from django.contrib import admin
from djangoarticle.models import CategoryModelScheme
from djangoarticle.models import ArticleModelScheme
from djangoarticle.modeladmins import CategoryModelSchemeAdmin
from djangoarticle.modeladmins import ArticleModelSchemeAdmin


# Register your models here.
admin.site.register(CategoryModelScheme, CategoryModelSchemeAdmin)
admin.site.register(ArticleModelScheme, ArticleModelSchemeAdmin)