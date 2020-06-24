from urllib.parse import urljoin

from django import template
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from django.templatetags.static import static
from django.utils.translation import get_language

from .models import SEOPath


register = template.Library()


def _get_meta_tags_from_context(context, path):
    flat_context = context.flatten()
    for obj in flat_context.values():
        if hasattr(obj, "get_absolute_url") and obj.get_absolute_url() == path:
            return obj, getattr(obj, "meta_tags", {})
    return (None, {})


def _get_meta_tags_for_path(path):
    return getattr(SEOPath.objects.filter(path=path).first(), "meta_tags", {})


def _collate_meta_tags(meta_tags):
    for language in getattr(settings, "SNAKEOIL_DEFAULT_TAGS", {}).keys():
        meta_tags[language] = {
            **settings.SNAKEOIL_DEFAULT_TAGS[language],
            **meta_tags.get(language, {}),
        }
    return meta_tags


def _get_meta_tags_for_language(meta_tags):
    if not settings.USE_I18N:
        return meta_tags.get("default", {})

    language = get_language()
    if "_" in language:
        language_tag = language[:2]
        specific_language_meta_tags = meta_tags.get(language, {})
        general_language_meta_tags = meta_tags.get(language_tag, {})
        all_language_meta_tags = {
            **general_language_meta_tags,
            **specific_language_meta_tags,
        }
    else:
        all_language_meta_tags = meta_tags.get(language, {})
    return {**meta_tags.get("default", {}), **all_language_meta_tags}


def _get_image_dimensions(obj, field_file):
    field = field_file.field
    if field.width_field:
        width = getattr(obj, field.width_field, field_file.width)
    else:
        width = field_file.width

    if field.height_field:
        height = getattr(obj, field.height_field, field_file.height)
    else:
        height = field_file.height
    return (width, height)


def _get_absolute_file_url(request, path):
    # Both Open Graph and Twitter Cards require absolute URLs.
    # Some static / media storages will give us absolute URLs.
    # However, the ones in Django, whitenoise, etc. just give relative URLs.
    # `urljoin()` will leave alone already-absolute URLs,
    # but we prefix relative URLs with the current site root.
    # If the sites framework is installed it uses the current site,
    # otherwise it will use data from the request object.
    # This should work for almost all cases.
    return urljoin(request.build_absolute_uri(), path)


def _parse_meta_tags(tags, request, obj=None):
    parsed_tags = {}
    for name, content in tags.items():
        if content.startswith("attr:"):
            if not obj:
                raise ValueError("Cannot use `attr:` without an object.")
            content = getattr(obj, content[5:])
            if isinstance(content, ImageFieldFile):
                field = content
                content = _get_absolute_file_url(request, field.url)
                if name in {"og:image", "og:image:url"}:
                    width, height = _get_image_dimensions(obj, field)
                    parsed_tags["og:image:width"] = width
                    parsed_tags["og:image:height"] = height
        elif content.startswith("static:"):
            content = _get_absolute_file_url(request, static(content[7:]))

        parsed_tags[name] = content
    return parsed_tags


def get_meta_tags(context, obj=None):
    """Fetch meta tags.

    1. If an object is passed, use it.
    2. If not, try to find the object in the context.
    3. If there isn't one, check if there is an object for the current path.
    4. Grab the defaults and merge in the tags from the model.
    5. Get tags based on the language.
    6. Return the tags.

    The priority works like this.
    - More specific languages beat less specific ones, e.g. en_GB > en > default.
    - Tags from the object beat tags from the settings.
    """
    if obj is not None:
        meta_tags = obj.meta_tags
    else:
        request_path = context["request"].path
        obj, meta_tags = _get_meta_tags_from_context(context, request_path)
        if not meta_tags:
            meta_tags = _get_meta_tags_for_path(request_path)

    meta_tags = _collate_meta_tags(meta_tags)
    meta_tags = _get_meta_tags_for_language(meta_tags)
    meta_tags = _parse_meta_tags(meta_tags, request=context["request"], obj=obj)

    return {
        "meta_tags": [
            {
                "attribute": "property" if name.startswith("og:") else "name",
                "name": name,
                "content": content,
            }
            for name, content in meta_tags.items()
        ]
    }
