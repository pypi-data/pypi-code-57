from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from snakeoil.models import SEOPath

from .models import Article


User = get_user_model()


class MetaTemplateTagTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="tom", first_name="Tom", last_name="Carrick"
        )
        cls.article = Article.objects.create(
            author=cls.user,
            slug="an-article",
            title="A test article",
            meta_tags={
                "default": {"description": "default description"},
                "en": {"description": "hello", "og:description": "opengraph hello"},
            },
        )

    def test_meta_template_tag_with_seo_model(self):
        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(response, '<meta name="description" content="hello">')
        self.assertContains(
            response, '<meta property="og:description" content="opengraph hello">'
        )

    def test_meta_template_tag_with_attr(self):
        self.article.meta_tags["en"]["author"] = "attr:author_name"
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertTemplateUsed(response, "tests/article_detail.html")
        self.assertContains(response, '<meta name="author" content="Tom Carrick">')

    def test_attr_with_object_from_context(self):
        self.article.meta_tags["en"]["author"] = "attr:author_name"
        self.article.save()

        response = self.client.get(
            f"/articles/{self.article.slug}/", {"template_without_obj": True}
        )

        self.assertTemplateUsed(response, "tests/article_detail_without_obj.html")
        self.assertContains(response, '<meta name="author" content="Tom Carrick">')

    def test_path(self):
        SEOPath.objects.create(
            path="/test-page/", meta_tags={"en": {"description": "path description"}}
        )

        response = self.client.get("/test-page/")

        self.assertContains(
            response, '<meta name="description" content="path description">'
        )

    def test_attr_not_allowed_for_path(self):
        SEOPath.objects.create(
            path="/test-page/",
            meta_tags={
                "en": {"description": "path description", "author": "attr:author_name"}
            },
        )
        with self.assertRaisesMessage(
            ValueError, "Cannot use `attr:` with an SEO Path."
        ):
            self.client.get("/test-page/")

    @override_settings(USE_I18N=False)
    def test_without_i18n(self):
        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response, '<meta name="description" content="default description">'
        )

    @override_settings(LANGUAGE_CODE="en_GB")
    def test_more_specific_language_wins(self):
        self.article.meta_tags["en_GB"] = {"description": "yorrite m8"}
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(response, '<meta name="description" content="yorrite m8">')

    @override_settings(LANGUAGE_CODE="en_GB")
    def test_fallback_to_generic_language(self):
        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(response, '<meta name="description" content="hello">')

    @override_settings(LANGUAGE_CODE="eo")
    def test_fallback_to_default(self):
        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response, '<meta name="description" content="default description">'
        )

    def test_image_field_with_width_and_height_fields(self):
        with open(settings.TESTS_DIR / "data" / "kitties.jpg", "rb") as f:
            self.article.main_image = SimpleUploadedFile(
                name="kitties.jpg", content=f.read(), content_type="image/jpeg",
            )
        self.article.meta_tags["en"] = {"og:image": "attr:main_image"}
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response,
            f'<meta property="og:image" content="{self.article.main_image.url}">',
        )
        self.assertContains(response, '<meta property="og:image:width" content="1577">')
        self.assertContains(response, '<meta property="og:image:height" content="889">')

    def test_image_field_without_width_and_height_fields(self):
        with open(settings.TESTS_DIR / "data" / "kitties.jpg", "rb") as f:
            self.article.secondary_image = SimpleUploadedFile(
                name="kitties.jpg", content=f.read(), content_type="image/jpeg",
            )
        self.article.meta_tags["en"] = {"og:image": "attr:secondary_image"}
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response,
            f'<meta property="og:image" content="{self.article.secondary_image.url}">',
        )
        self.assertContains(response, '<meta property="og:image:width" content="1577">')
        self.assertContains(response, '<meta property="og:image:height" content="889">')

    def test_attr_manual_image(self):
        # The field here doesn't matter. It should just get passed through.
        # This is to handle URLFields, etc.
        self.article.meta_tags["en"]["og:image"] = "attr:slug"
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response, '<meta property="og:image" content="an-article">',
        )

    def test_static(self):
        # The default finder doesn't care if the file exists or not.
        self.article.meta_tags["en"]["og:image"] = "static:foo/dummy.png"
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertContains(
            response, '<meta property="og:image" content="/static/foo/dummy.png">'
        )

    @override_settings(SNAKEOIL_DEFAULT_TAGS={"default": {"og:site_name": "My Site"}})
    def test_default_tags(self):
        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertNotIn("og:site_name", self.article.meta_tags.get("en", {}))
        self.assertNotIn("og:site_name", self.article.meta_tags.get("default", {}))
        self.assertContains(
            response, '<meta property="og:site_name" content="My Site">'
        )
        self.assertContains(response, '<meta name="description" content="hello">')
        self.assertContains(
            response, '<meta property="og:description" content="opengraph hello">'
        )

    @override_settings(SNAKEOIL_DEFAULT_TAGS={"default": {"og:site_name": "My Site"}})
    def test_model_beats_defaults(self):
        self.article.meta_tags["default"]["og:site_name"] = "Not really my site"
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertNotContains(
            response, '<meta property="og:site_name" content="My Site">'
        )
        self.assertContains(
            response, '<meta property="og:site_name" content="Not really my site">'
        )

    @override_settings(
        LANGUAGE_CODE="eo",
        SNAKEOIL_DEFAULT_TAGS={"eo": {"og:site_name": "Mia Esperanta Retejo"}},
    )
    def test_language_default_beats_model(self):
        self.article.meta_tags["default"]["og:site_name"] = "My Site"
        self.article.save()

        response = self.client.get(f"/articles/{self.article.slug}/")

        self.assertNotContains(
            response, '<meta property="og:site_name" content="My Site">'
        )
        self.assertContains(
            response, '<meta property="og:site_name" content="Mia Esperanta Retejo">'
        )
