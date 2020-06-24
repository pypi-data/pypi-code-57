from django.contrib.auth import get_user_model
from django.test import TestCase

from snakeoil.models import SEOPath

from .models import Article


User = get_user_model()


class SeoModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="tom")
        cls.article = Article.objects.create(
            author=cls.user, slug="an-article", title="A test article"
        )

    def test_add_meta_tags_to_model(self):
        self.article.meta_tags = {
            "en": {"description": "hello", "og:description": "also hello"}
        }
        self.article.save()
        self.article.refresh_from_db()
        meta_tags = self.article.meta_tags
        self.assertEqual(meta_tags["en"]["description"], "hello")
        self.assertEqual(meta_tags["en"]["og:description"], "also hello")

    def test_add_seo_path(self):
        seo_path = SEOPath.objects.create(
            path="/test-page/", meta_tags={"default": {"description": "hello"}}
        )
        self.assertEqual(str(seo_path), "/test-page/")
