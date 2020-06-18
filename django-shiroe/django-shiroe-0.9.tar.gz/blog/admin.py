from django.contrib import admin
from django import forms
from django.utils.translation import gettext as _
from . import models


class BaseAdminForm(forms.ModelForm):
    def clean_slug(self):
        """Show error to user if name is duplciated"""
        slug = self.cleaned_data["slug"]
        if type(self.instance).objects.filter(slug=slug).exists():
            raise forms.ValidationError("This object already exists")
        return slug


class PostAdminForm(BaseAdminForm):
    class Meta:
        model = models.Post
        fields = "__all__"


class TagAdminForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = ("name",)

    def clean_slug(self):
        """Show error to user if name is duplicated."""
        slug = self.cleaned_data["slug"]
        print(slug, "SLUUUUUUUUG")
        if models.Tag.objects.filter(slug=slug).exists():
            raise forms.ValidationError("This object already exists")
        return slug


class CategoryAdminForm(BaseAdminForm):
    class Meta:
        model = models.Category
        fields = "__all__"


class SocialAccountAdminForm(BaseAdminForm):
    class Meta:
        model = models.Tag
        fields = "__all__"


class PostAdmin(admin.ModelAdmin):

    """This allows authenticated users to manage blog posts."""

    ordering = ("-created_at",)
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "file_type",
        "created_at",
        "modified_at",
    )
    fieldsets = (
        (_("Author"), {"fields": ("author",)}),
        (
            _("Blog Post"),
            {"fields": ("cover_image", "title", "slug", "content", "summary", "tags")},
        ),
        (_("Options"), {"fields": ("status", "file_type")}),
        (_("Misc"), {"fields": ("created_at", "modified_at",)}),
    )
    readonly_fields = (
        "created_at",
        "modified_at",
    )
    form = PostAdminForm


class AuthorAdmin(admin.ModelAdmin):
    ordering = ("-created_at",)
    list_display = (
        "first_name",
        "last_name",
        "slug",
    )
    fields = ("user", "avatar", "first_name", "last_name", "description")
    readonly_fields = (
        "slug",
        "created_at",
        "modified_at",
    )


class TagAdmin(admin.ModelAdmin):
    ordering = ("-created_at",)
    readonly_fields = (
        "slug",
        "created_at",
        "modified_at",
    )
    form = TagAdminForm


class CategoryAdmin(admin.ModelAdmin):
    ordering = ("-created_at",)
    readonly_fields = (
        "slug",
        "created_at",
        "modified_at",
    )
    form = CategoryAdminForm


class SocialAccountAdmin(admin.ModelAdmin):
    ordering = ("-created_at",)
    readonly_fields = (
        "slug",
        "created_at",
        "modified_at",
    )
    form = SocialAccountAdminForm


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.SocialAccount, SocialAccountAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)
