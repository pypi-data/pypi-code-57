import tempfile
import uuid

from PIL import Image
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from .. import models


class AuthorTestCase(TestCase):
    """Testing the Author Model"""

    def setUp(self) -> None:
        self.first_name = "Test"
        self.last_name = "User"
        self.email = "test@example.com"
        user_data = {
            f"{get_user_model().USERNAME_FIELD}": self.email,
            "password": "12345678uhgvb",
        }
        self.user = get_user_model().objects.create_user(**user_data)
        self.mock_image = self.get_mock_image()

    def tearDown(self) -> None:
        self.user.delete()

    @staticmethod
    def get_mock_image():
        from django.core.files.images import ImageFile

        file = tempfile.NamedTemporaryFile(suffix=".png")
        return ImageFile(file, name=file.name)

    def test_author_creation_success(self) -> None:
        """Test author can be created with valid details"""
        author = models.Author.objects.create(
            user=self.user,
            avatar=self.mock_image,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        author_exists = models.Author.objects.filter(user=self.user).exists()
        self.assertTrue(author_exists)
        self.assertTrue(author.avatar)
        self.assertEqual(author.first_name, self.first_name)
        self.assertEqual(author.last_name, self.last_name)

    def test_author_creation_fail_no_user(self) -> None:
        """Test author creation fails if no user obj is provided"""
        with self.assertRaises(get_user_model().DoesNotExist):
            models.Author.objects.create(
                avatar=self.mock_image,
                first_name=self.first_name,
                last_name=self.last_name,
            )

    def test_author_creation_fail_no_first_name(self) -> None:
        """Test author creation fails if no first_name is provided"""
        with self.assertRaises(ValidationError):
            models.Author.objects.create(
                user=self.user, avatar=self.mock_image, last_name=self.last_name,
            )

    def test_author_creation_fail_no_last_name(self) -> None:
        """Test author creation fails if no last_name is provided"""
        with self.assertRaises(ValidationError):
            models.Author.objects.create(
                user=self.user, avatar=self.mock_image, first_name=self.first_name,
            )

    def test_author_creation_fail_invalid_name(self) -> None:
        """Test author creation fails if invalid_name is provided"""
        with self.assertRaises(ValidationError):
            models.Author.objects.create(
                user=self.user,
                avatar=self.mock_image,
                first_name="1234567",
                last_name="1234567",
            )


class PostTestCase(TestCase):
    """Testing the Post Model"""

    def setUp(self) -> None:
        self.title = "Blog title example"
        self.content = "I'm just a blog content "
        self.category_name = "General"
        self.email = "author@example.com"
        self.author = self.create_author()
        self.category = self.create_category()

    def tearDown(self) -> None:
        self.author.user.delete()
        self.author.delete()
        self.category.delete()

    def create_author(self, **kwargs) -> models.Author:
        """Create a sample author"""
        author_data = {
            f"{get_user_model().USERNAME_FIELD}": self.email,
            "password": "1239i9rg",
        }
        author_data.update(kwargs)
        user = get_user_model().objects.create_user(**author_data)
        author = models.Author.objects.create(
            user=user, first_name="Test", last_name="User"
        )
        return author

    @staticmethod
    def get_mock_image():
        from django.core.files.images import ImageFile

        file = tempfile.NamedTemporaryFile(suffix=".png")
        return ImageFile(file, name=file.name)

    def create_category(self, **kwargs) -> models.Category:
        defaults = {"name": self.category_name}
        defaults.update(kwargs)
        category = models.Category.objects.create(**defaults)
        return category

    def test_post_creation_success_valid_details(self) -> None:
        """Test post can be created when valid details are supplied"""
        title = content = uuid.uuid4()
        post = models.Post.objects.create(
            author=self.author,
            title=title,
            content=content,
            category=self.category,
            cover_image=self.get_mock_image(),
        )
        author_and_categories_exist = models.Post.objects.filter(
            slug=post.slug, author=self.author, category=self.category
        ).exists()
        post_exists = models.Post.objects.filter(
            author=self.author, title=title, content=content, category=self.category
        ).exists()
        self.assertTrue(post_exists)
        self.assertTrue(post.cover_image)
        self.assertEqual(post.title, title)
        self.assertEqual(post.slug, slugify(title))
        self.assertTrue(author_and_categories_exist)
        self.assertEqual(post.file_type, models.Post.HTML)
        self.assertEqual(post.status, models.Post.DRAFT)
        self.assertEqual(post.created_at, post.modified_at)

    def test_post_creation_success_no_author(self) -> None:
        """Test post can be created when valid details are supplied but no author"""
        title = content = uuid.uuid4()
        post = models.Post.objects.create(
            title=title, content=content, category=self.category,
        )
        post_exists = models.Post.objects.filter(
            title=title, content=content, category=self.category
        ).exists()
        self.assertTrue(post_exists)
        self.assertEqual(post.title, title)
        self.assertEqual(post.author, None)
        self.assertEqual(post.slug, slugify(title))
        self.assertEqual(post.file_type, models.Post.HTML)
        self.assertEqual(post.created_at, post.modified_at)

    def test_post_creation_success_no_category(self) -> None:
        """Test post can be created when valid details are supplied but no category"""
        title = content = uuid.uuid4()
        post = models.Post.objects.create(
            author=self.author, title=title, content=content,
        )
        post_exists = models.Post.objects.filter(
            author=self.author, title=title, content=content
        ).exists()
        self.assertTrue(post_exists)
        self.assertEqual(post.title, title)
        self.assertEqual(post.slug, slugify(title))
        self.assertEqual(post.file_type, models.Post.HTML)
        self.assertEqual(post.created_at, post.modified_at)

    def test_post_creation_success_no_cover_image(self) -> None:
        """Test post can be created when valid details
        are supplied but no cover_image"""
        title = content = uuid.uuid4()
        post = models.Post.objects.create(
            title=title, content=content, category=self.category, author=self.author
        )
        post_exists = models.Post.objects.filter(
            author=self.author, title=title, content=content, category=self.category
        ).exists()
        self.assertTrue(post_exists)
        self.assertEqual(post.title, title)
        self.assertEqual(post.cover_image, None)
        self.assertEqual(post.author, self.author)
        self.assertEqual(post.slug, slugify(title))
        self.assertEqual(post.file_type, models.Post.HTML)
        self.assertEqual(post.created_at, post.modified_at)

    def test_post_tags_addition_success(self) -> None:
        """Test tag can be successfully created"""
        title = content = uuid.uuid4()
        post = models.Post.objects.create(
            author=self.author,
            title=title,
            content=content,
            category=self.category,
            cover_image=self.get_mock_image(),
        )
        tag = models.Tag.objects.create(name="General")
        tag2 = models.Tag.objects.create(name="General2")
        post.tags.add(tag, tag2)
        tags_exist = models.Post.objects.filter(
            slug=post.slug, tags__slug__in=[tag.slug, tag2.slug]
        ).exists()
        self.assertTrue(tags_exist)
        self.assertEqual(post.tags.count(), 2)

    def test_post_creation_fail_no_title(self) -> None:
        """Test post creation fails if no title is supplied"""
        with self.assertRaises(ValidationError):
            content = uuid.uuid4()
            models.Post.objects.create(
                author=self.author, content=content, category=self.category
            )

    def test_post_creation_fail_no_content(self) -> None:
        """Test post creation fails if no content is supplied"""
        with self.assertRaises(ValidationError):
            title = uuid.uuid4()
            models.Post.objects.create(
                author=self.author, title=title, category=self.category
            )

    def test_post_marked_as_published(self) -> None:
        """Test that post is marked as published after running publish method"""
        title = self.title
        content = self.content
        post = models.Post.objects.create(
            author=self.author, title=title, content=content, category=self.category,
        )
        self.assertEqual(post.status, models.Post.DRAFT)

        # Publish post
        post.mark_as_published()
        post.refresh_from_db()
        self.assertEqual(post.status, models.Post.PUBLISHED)

    def test_post_marked_as_draft(self) -> None:
        """Test that post is marked as draft after running draft method"""
        post = models.Post.objects.create(
            author=self.author,
            title=self.title,
            content=self.content,
            category=self.category,
            status=models.Post.PUBLISHED,
        )
        self.assertEqual(post.status, models.Post.PUBLISHED)

        # Publish post
        post.mark_as_draft()
        post.refresh_from_db()
        self.assertEqual(post.status, models.Post.DRAFT)


class CategoryTestCase(TestCase):
    """Testing the category model"""

    def setUp(self) -> None:
        self.name = "General"

    def test_category_creation_success(self) -> None:
        """Test category can be created successfully"""
        models.Category.objects.create(name=self.name)
        category_exists = models.Category.objects.filter(
            slug=slugify(self.name)
        ).exists()
        self.assertTrue(category_exists)


class TagTestCase(TestCase):
    """Testing the tags model"""

    def setUp(self) -> None:
        self.name = "General-Small"

    def test_category_creation_success(self) -> None:
        """Test tag can be created successfully"""
        models.Tag.objects.create(name=self.name)
        tag_exists = models.Tag.objects.filter(slug=slugify(self.name)).exists()
        self.assertTrue(tag_exists)
