import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.shortcuts import reverse

from rest_framework import status
from rest_framework.test import APIClient

from ..models import Author, SocialAccount, Post, Category, Tag


class AuthorPublicApi(TestCase):
    """Testing author endpoint as an unauthorized user"""

    def setUp(self) -> None:
        """Setup method for each test"""
        self.endpoint = reverse("blog:author-list")
        self.client = APIClient()
        user_data = {
            f"{get_user_model().USERNAME_FIELD}": "test@example.com",
            "password": "12345ABC.//",
        }
        self.user = get_user_model().objects.create_user(**user_data)

    @staticmethod
    def _create_author(**kwargs):
        return Author.objects.create(**kwargs)

    @staticmethod
    def author_detail_endpoint(slug: str) -> None:
        """Return author detail url"""
        return reverse("blog:author-detail", args=[slug])

    def test_get_authors_success(self) -> None:
        """Test get request returns 200 for unauthenticated users """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_authors_failure(self) -> None:
        """Test post request returns unauthorized for unauthenticated users """
        response = self.client.post(self.endpoint, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Author.objects.count(), 0)

    def test_put_authors_failure(self) -> None:
        """Test put request returns unauthorized for unauthenticated users """
        author = self._create_author(
            user=self.user, first_name="Aaron", last_name="Kazah"
        )
        response = self.client.put(self.author_detail_endpoint(author.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_authors_failure(self) -> None:
        """Test patch request returns unauthorized for unauthenticated users """
        author = self._create_author(
            user=self.user, first_name="Aaron", last_name="Kazah"
        )
        response = self.client.patch(self.author_detail_endpoint(author.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_authors_failure(self) -> None:
        """Test delete request returns unauthorized for unauthenticated users """
        author = self._create_author(user=self.user, first_name="Ben", last_name="10")
        response = self.client.delete(self.author_detail_endpoint(author.slug))
        author = Author.objects.filter(slug="ben-10")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(author.exists(), True)


class AuthorPrivateApi(TestCase):
    """Testing author endpoint as an authorized user """

    def setUp(self) -> None:
        """Setup method for each test """
        self.first_name = "Aaron"
        self.last_name = "Test"
        self.email = "test@example.com"
        self.password = "password123..."
        self.endpoint = reverse("blog:author-list")
        self.client = APIClient()
        user_data = {
            f"{get_user_model().USERNAME_FIELD}": self.email,
            "password": self.password,
        }
        self.user = get_user_model().objects.create_user(**user_data)
        self.client.force_authenticate(self.user)

    def tearDown(self) -> None:
        self.user.delete()

    @staticmethod
    def author_detail_endpoint(author_slug: str) -> None:
        """Return author detail url """
        return reverse("blog:author-detail", args=[author_slug])

    @staticmethod
    def _create_author(**kwargs):
        return Author.objects.create(**kwargs)

    def test_get_authors_success(self) -> None:
        """Test get request returns 200 for authenticated users """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_author_success(self) -> None:
        """Test post request returns 200 for authenticated users """
        payload = {"first_name": "Jack", "last_name": "awefwen", "user": self.user.id}
        response = self.client.post(self.endpoint, data=payload)
        author = Author.objects.filter(**payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(author.exists())
        self.assertEqual(author.first().first_name, payload["first_name"])
        self.assertEqual(author.first().last_name, payload["last_name"])
        self.assertEqual(author.first().user.id, payload["user"])

    def test_put_author_fail(self) -> None:
        """Test PUT request returns 405"""
        author = self._create_author(
            user=self.user, first_name="Aaron", last_name="Kazah"
        )
        payload = {
            "last_name": "Burgers",
        }
        response = self.client.put(
            self.author_detail_endpoint(author.slug), data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_author_success(self) -> None:
        """Test PATCH request returns 200"""
        author = self._create_author(
            user=self.user, first_name="Aaron", last_name="Kazah"
        )
        payload = {
            "last_name": "Burgers",
        }
        response = self.client.patch(
            self.author_detail_endpoint(author.slug), data=payload
        )
        author.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(author.last_name, payload["last_name"])

    def test_delete_author_success(self) -> None:
        """Test DELETE request returns 200"""
        author = self._create_author(
            user=self.user, first_name="Mary", last_name="Donalds"
        )
        response = self.client.delete(self.author_detail_endpoint(author.slug))
        author = Author.objects.filter(
            user=self.user, first_name="Mary", last_name="Donalds"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(author.exists(), False)


class SocialAccountPublicAPi(TestCase):
    """Testing social account endpoint as an unauthorized user """

    def setUp(self) -> None:
        """Setup method for each test """
        self.endpoint = reverse("blog:social_account-list")
        self.client = APIClient()

    @staticmethod
    def social_account_detail_endpoint(slug: str) -> None:
        """Return social account detail url """
        return reverse("blog:social_account-detail", args=[slug])

    def test_get_social_accounts_success(self) -> None:
        """Test get request returns 200 for unauthenticated users """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_social_accounts_fail(self) -> None:
        """Test post request returns unauthorized for unauthenticated users """
        response = self.client.post(self.endpoint, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(SocialAccount.objects.count(), 0)

    def test_patch_social_accounts_fail(self) -> None:
        """Test patch request returns unauthorized for unauthenticated users """
        social_account = SocialAccount.objects.create(name="General")
        response = self.client.patch(
            self.social_account_detail_endpoint(social_account.slug), {}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_social_accounts_fail(self) -> None:
        """Test put request returns method not allowed """
        social_account = SocialAccount.objects.create(name="General")
        response = self.client.put(
            self.social_account_detail_endpoint(social_account.slug), {}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_social_accounts(self) -> None:
        """Test delete request returns unauthorized """
        social_account = SocialAccount.objects.create(name="General")
        response = self.client.delete(
            self.social_account_detail_endpoint(social_account.slug), {}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SocialAccountPrivateAPi(TestCase):
    """Testing social account endpoint as an authorized user """

    def setUp(self) -> None:
        """Setup method for each test """
        self.first_name = "Aaron"
        self.last_name = "Test"
        self.email = "test@example.com"
        self.password = "password123..."
        self.endpoint = reverse("blog:social_account-list")
        self.client = APIClient()
        user_data = {
            f"{get_user_model().USERNAME_FIELD}": self.email,
            "password": self.password,
        }
        self.user = get_user_model().objects.create_user(**user_data)
        self.client.force_authenticate(self.user)

    def tearDown(self) -> None:
        self.user.delete()

    @staticmethod
    def social_account_detail_endpoint(slug: str) -> None:
        """Return social account detail url """
        return reverse("blog:social_account-detail", args=[slug])

    @staticmethod
    def _social_account(**kwargs):
        return SocialAccount.objects.create(**kwargs)

    def test_get_social_account_success(self) -> None:
        """Test get request returns 200 for authenticated users """
        _ = self._social_account(name="Twitter")
        response = self.client.get(self.endpoint)
        twitter = SocialAccount.objects.filter(slug="twitter")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(twitter.exists(), True)

    def test_post_social_account_success(self) -> None:
        """Test POST request returns 200 """
        payload = {"name": "Google", "url": "google.com"}
        response = self.client.post(self.endpoint, data=payload)
        google = SocialAccount.objects.filter(**payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(google.exists())

    def test_put_social_account_fail(self) -> None:
        """Test PUT request returns 405 """
        twitter = self._social_account(name="Twitter")
        payload = {
            "name": "Google",
        }
        response = self.client.put(
            self.social_account_detail_endpoint(twitter.slug), data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_social_account_success(self) -> None:
        """Test PATCH request returns 200 """
        twitter = self._social_account(name="Twitter")
        payload = {
            "name": "Google",
        }
        response = self.client.patch(
            self.social_account_detail_endpoint(twitter.slug), data=payload
        )
        twitter.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(twitter.name, payload["name"])

    def test_delete_social_account_success(self) -> None:
        """Test DELETE request returns 200 """
        twitter = self._social_account(name="Twitter")
        response = self.client.delete(self.social_account_detail_endpoint(twitter.slug))
        social_account = SocialAccount.objects.filter(slug="twitter")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(social_account.exists(), False)


class CategoryPublicApi(TestCase):
    """Testing Category api for unauthorized users """

    def setUp(self) -> None:
        """Setup method for each test """
        self.endpoint = reverse("blog:category-list")
        self.client = APIClient()

    @staticmethod
    def category_endpoint(slug: str) -> None:
        """Return category detail url """
        return reverse("blog:category-detail", args=[slug])

    def test_get_categories_success(self) -> None:
        """Test get request returns 200 for unauthenticated users """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_categories_fail(self) -> None:
        """Test post request returns unauthorized for unauthenticated users """
        response = self.client.post(self.endpoint, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Category.objects.count(), 0)

    def test_patch_categories_fail(self) -> None:
        """Test patch request returns unauthorized for unauthenticated users """
        category = Category.objects.create(name="Spongebob")
        response = self.client.patch(self.category_endpoint(category.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_categories_fail(self) -> None:
        """Test put request returns method not allowed """
        category = Category.objects.create(name="Spongebob")
        response = self.client.put(self.category_endpoint(category.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_category_accounts(self) -> None:
        """Test delete request returns unauthorized """
        category = Category.objects.create(name="Spongebob")
        response = self.client.patch(self.category_endpoint(category.slug))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CategoryPrivateApi(TestCase):
    """Testing Category endpoint as an authorized user """

    def setUp(self) -> None:
        self.first_name = "Aaron"
        self.last_name = "Test"
        self.email = "test@example.com"
        self.password = "password123..."
        self.endpoint = reverse("blog:category-list")
        self.client = APIClient()
        user_data = {
            f"{get_user_model().USERNAME_FIELD}": self.email,
            "password": self.password,
        }
        self.user = get_user_model().objects.create_user(**user_data)
        self.client.force_authenticate(self.user)

    def tearDown(self) -> None:
        self.user.delete()

    @staticmethod
    def category_endpoint(slug: str) -> None:
        """Return social account detail url """
        return reverse("blog:category-detail", args=[slug])

    @staticmethod
    def _category(**kwargs):
        return Category.objects.create(**kwargs)

    def test_get_category_success(self) -> None:
        """Test get request returns 200 for authenticated users """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_category_success(self) -> None:
        """Test POST request returns 200 """
        payload = {"name": "Pink"}
        response = self.client.post(self.endpoint, data=payload)
        category = Category.objects.filter(**payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(category.exists())

    def test_put_category_fail(self) -> None:
        """Test PUT request returns 405 """
        category = self._category(name="Pink")
        payload = {
            "name": "Red",
        }
        response = self.client.put(self.category_endpoint(category.slug), data=payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_category_success(self) -> None:
        """Test PATCH request returns 200 """
        category = self._category(name="Yellow")
        payload = {
            "name": "Blue",
        }
        response = self.client.patch(
            self.category_endpoint(category.slug), data=payload
        )
        category.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(category.name, payload["name"])

    def test_delete_category_success(self) -> None:
        """Test DELETE request returns 200 """
        category = self._category(name="Twitter")
        response = self.client.delete(self.category_endpoint(category.slug))
        category = Category.objects.filter(slug="twitter")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(category.exists(), False)


class TagPublicApi(TestCase):
    """Testing Tag api for unauthorized users """

    def setUp(self) -> None:
        """Setup method for each test """
        self.endpoint = reverse("blog:tag-list")
        self.client = APIClient()

    @staticmethod
    def tag_endpoint(slug: str) -> None:
        """Return social account detail url """
        return reverse("blog:tag-detail", args=[slug])

    def test_get_tags_success(self) -> None:
        """Test get request returns 200 for unauthenticated users """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_tags_fail(self) -> None:
        """Test post request returns unauthorized for unauthenticated users """
        response = self.client.post(self.endpoint, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_tags_fail(self) -> None:
        """Test patch request returns unauthorized for unauthenticated users """
        tag = Tag.objects.create(name="tag")
        response = self.client.patch(self.tag_endpoint(tag.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_tags_fail(self) -> None:
        """Test put request returns method not allowed """
        tag = Tag.objects.create(name="tag")
        response = self.client.put(self.tag_endpoint(tag.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_tags_accounts(self) -> None:
        """Test delete request returns unauthorized """
        tag = Tag.objects.create(name="tag")
        response = self.client.delete(self.tag_endpoint(tag.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TagPrivateApi(TestCase):
    """Testing Category endpoint as an authorized user """

    def setUp(self) -> None:
        self.first_name = "Aaron"
        self.last_name = "Test"
        self.email = "test@example.com"
        self.password = "password123..."
        self.endpoint = reverse("blog:tag-list")
        self.client = APIClient()
        user_data = {
            f"{get_user_model().USERNAME_FIELD}": self.email,
            "password": self.password,
        }
        self.user = get_user_model().objects.create_user(**user_data)
        self.client.force_authenticate(self.user)

    def tearDown(self) -> None:
        self.user.delete()

    @staticmethod
    def tag_endpoint(slug: str) -> None:
        """Return social account detail url """
        return reverse("blog:tag-detail", args=[slug])

    @staticmethod
    def _create_tag(**kwargs):
        return Tag.objects.create(**kwargs)

    def test_get_tag_success(self) -> None:
        """Test get request returns 200 for authenticated users """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_tag_success(self) -> None:
        """Test POST request returns 200 """
        payload = {"name": "B2B"}
        response = self.client.post(self.endpoint, data=payload)
        tag = Tag.objects.filter(**payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(tag.exists())

    def test_put_tag_fail(self) -> None:
        """Test PUT request returns 405 """
        tag = self._create_tag(name="Pink")
        payload = {
            "name": "Red",
        }
        response = self.client.put(self.tag_endpoint(tag.slug), data=payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_tag_success(self) -> None:
        """Test PATCH request returns 200 """
        tag = self._create_tag(name="Green")
        payload = {
            "name": "Blue",
        }
        response = self.client.patch(self.tag_endpoint(tag.slug), data=payload)
        tag.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(tag.name, payload["name"])

    def test_delete_tag_success(self) -> None:
        """Test DELETE request returns 200 """
        tag = self._create_tag(name="twitter")
        response = self.client.delete(self.tag_endpoint(tag.slug))
        tag = Tag.objects.filter(slug="twitter")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(tag.exists(), False)


class PostPublicApi(TestCase):
    """Testing POST endpoint as an unauthorized user """

    def setUp(self) -> None:
        """Setup method for each test """
        self.endpoint = reverse("blog:post-list")
        self.client = APIClient()
        user_data = {
            f"{get_user_model().USERNAME_FIELD}": "test@example.com",
            "password": "12345ABC.//",
        }
        self.user = get_user_model().objects.create_user(**user_data)

    @staticmethod
    def _create_post(**kwargs):
        return Post.objects.create(**kwargs)

    @staticmethod
    def post_detail_endpoint(slug: str) -> None:
        """Return blog post detail url """
        return reverse("blog:post-detail", args=[slug])

    def test_get_blog_post_success(self) -> None:
        """Test get request returns 200 for unauthenticated users """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_blog_post_failure(self) -> None:
        """Test post request returns unauthorized for unauthenticated users """
        response = self.client.post(self.endpoint, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)

    def test_put_blog_post_failure(self) -> None:
        """Test put request returns unauthorized for unauthenticated users """
        post = self._create_post(title="Test Title", content="Test content")
        response = self.client.put(self.post_detail_endpoint(post.slug), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_blog_post_failure(self) -> None:
        """Test patch request returns unauthorized for unauthenticated users """
        post = self._create_post(title="Test Title", content="Test content")
        payload = {"title": "banana"}
        response = self.client.patch(self.post_detail_endpoint(post.slug), payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(post.title, payload["title"])

    def test_delete_blog_post_failure(self) -> None:
        """Test delete request returns unauthorized for unauthenticated users """
        post = self._create_post(title="Test Title", content="Test content")
        response = self.client.delete(self.post_detail_endpoint(post.slug), {})
        post = Post.objects.filter(slug="test-title")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(post.exists(), True)


class PostPrivateAPI(TestCase):
    """Testing post endpoint as an authorized user """

    def setUp(self) -> None:
        """Setup method for each test """
        self.first_name = "Aaron"
        self.last_name = "Test"
        self.email = "test@example.com"
        self.password = "password123..."
        self.endpoint = reverse("blog:post-list")
        self.client = APIClient()
        user_data = {
            f"{get_user_model().USERNAME_FIELD}": self.email,
            "password": self.password,
        }
        self.user = get_user_model().objects.create_user(**user_data)
        self.client.force_authenticate(self.user)

    def tearDown(self) -> None:
        self.user.delete()

    @staticmethod
    def _create_post(**kwargs):
        return Post.objects.create(**kwargs)

    @staticmethod
    def detail_endpoint(slug: str) -> None:
        """Return author detail url """
        return reverse("blog:post-detail", args=[slug])

    def test_get_blog_post_success(self) -> None:
        """Test get request returns 200 for unauthenticated users """
        response = self.client.get(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_blog_post_success(self) -> None:
        """Test post request returns unauthorized for unauthenticated users """
        payload = {"title": "Test title", "content": "Test description"}
        response = self.client.post(self.endpoint, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_put_blog_post_fail(self) -> None:
        """Test put request returns unauthorized for unauthenticated users """
        post = self._create_post(title="Test Title", content="Test content")
        response = self.client.put(self.detail_endpoint(post.slug), {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_blog_post_success(self) -> None:
        """Test patch request return 200 OK """
        post = self._create_post(title="Test Title", content="Test content")
        payload = {"title": "banana"}
        response = self.client.patch(self.detail_endpoint(post.slug), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(post.title, payload["title"])

    def test_patch_blog_post_tags_success(self) -> None:
        """Test that tags are successfully added """
        post = self._create_post(title="Test Title", content="Test content")
        payload = {"tags": ["banana", "apple", "sugar"]}
        response = self.client.patch(self.detail_endpoint(post.slug), payload)
        post.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.tags.count(), len(payload["tags"]))
        self.assertTrue(post.tags.filter(slug__in=payload["tags"]).exists())

    def test_patch_blog_post_tags_removal(self) -> None:
        """Test that tags are successfully removed """
        post = self._create_post(title="Test tTitle", content="Test content")
        payload = {"tags": []}
        response = self.client.patch(self.detail_endpoint(post.slug), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.tags.count(), 0)
        self.assertFalse(post.tags.filter(slug__in=payload["tags"]).exists())

    def test_delete_blog_post_success(self) -> None:
        """Test delete request returns unauthorized for unauthenticated users """
        post = self._create_post(title="Test Title", content="Test content")
        response = self.client.delete(self.detail_endpoint(post.slug), {})
        post = Post.objects.filter(slug="test-title")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(post.exists(), False)
