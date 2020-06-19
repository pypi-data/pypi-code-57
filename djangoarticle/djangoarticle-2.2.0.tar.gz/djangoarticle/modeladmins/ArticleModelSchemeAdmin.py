from django.contrib import admin
from django.db import models
from django import forms


class ArticleModelSchemeAdmin(admin.ModelAdmin):
    list_display        = ['title', 'category', 'author', 'verification', 'status']
    list_filter         = ['created_at', 'updated_at', 'status']
    search_fields       = ['title', 'slug']
    prepopulated_fields = {'slug' : ('title',)}
    list_per_page       = 10
    actions             = ['make_verified', 'make_published']
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size':'35'})},
        models.IntegerField: {'widget': forms.NumberInput(attrs={'size': '35'})}
    }
    fieldsets           = (
        ('Basic Informations', {
            'fields': ['serial', ('title', 'slug')]
        }),
        ('Article Category', {
            'fields': ['category']
        }),
        ('Media Files', {
            'classes': ['collapse', 'extrapretty'],
            'fields': ['cover_image']
        }),
        ('Description', {
            'classes': ['collapse', 'extrapretty'],
            'fields': ['description']
        }),
        ('Shortlines', {
            'classes': ['collapse', 'extrapretty'],
            'fields': ['shortlines']
        }),
        ('Content', {
            'classes': ['collapse', 'extrapretty'],
            'fields': ['content']
        }),
        ('Article Views', {
            'classes': ['collapse', 'extrapretty'],
            'fields': ['total_views']
        }),
        ('Article Status', {
            'fields': [('verification', 'is_promote', 'is_trend', 'is_promotional', 'is_opinion'), 'author', 'status']
        }),
        ('Tags', {
            'classes': ['collapse', 'extrapretty'],
            'fields': ['tags']
        })
    )

    def make_verified(self, request, queryset):
        row_updated = queryset.update(verification=True)
        if row_updated == 1:
            message_bit = '1 article was'
        else:
            message_bit = f'{row_updated} articles were'
        self.message_user(request, f'{message_bit} verified successfully.')

    make_verified.short_description = 'make articles verified'
    make_verified.allowed_permissions = ('change',)

    def make_published(self, request, queryset):
        row_updated = queryset.update(status='publish')
        if row_updated == 1:
            message_bit = '1 article was'
        else:
            message_bit = f'{row_updated} articles were'
        self.message_user(request, f'{message_bit} published successfully.')

    make_published.short_description = 'make articles published'
    make_published.allowed_permissions = ('change',)