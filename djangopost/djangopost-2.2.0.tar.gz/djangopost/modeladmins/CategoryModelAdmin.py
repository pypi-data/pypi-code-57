from django.contrib import admin
from django.db import models
from django import forms


class CategoryModelAdmin(admin.ModelAdmin):
    list_display        = ['title', 'author', 'verification', 'status']
    list_filter         = ['created_at', 'updated_at', 'status']
    search_fields       = ['title',]
    prepopulated_fields = {'slug' : ('title',)}
    list_per_page       = 10
    actions             = ['make_verified', 'make_published']
    formfield_overrides = {
        models.IntegerField: {'widget': forms.NumberInput(attrs={'size': '35'})},
        models.CharField: {'widget': forms.TextInput(attrs={'size': '35'})},
        models.SlugField: {'widget': forms.TextInput(attrs={'size': '35'})}
    }
    fieldsets           = (
        ('Basic informations', {
            'classes': ['extrapretty'],
            'fields': ['serial', ('title', 'slug')]
        }),
        ('Description', {
            'classes': ['collapse', 'extrapretty'],
            'fields': ['description',]
        }),
        ('Category Status', {
            'classes': ['collapse', 'extrapretty'],
            'fields': ['verification', 'author', 'status']
        })
    )

    def make_verified(self, request, queryset):
        row_updated = queryset.update(verification=True)
        if row_updated == 1:
            message_bit = '1 category was'
        else:
            message_bit = f'{row_updated} categories were'
        self.message_user(request, f'{message_bit} verified successfully.')

    make_verified.short_description = 'make categories verified'
    make_verified.allowed_permissions = ('change',)

    def make_published(self, request, queryset):
        row_updated = queryset.update(status='publish')
        if row_updated == 1:
            message_bit = '1 category was'
        else:
            message_bit = f'{row_updated} categories were'
        self.message_user(request, f'{message_bit} published successfully.')

    make_published.short_description = 'make categories published'
    make_published.allowed_permissions = ('change',)