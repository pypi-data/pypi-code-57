import uuid

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from blog.models import Author, Tag, Category, Post, SocialAccount


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = uuid.uuid4()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@gmail.com", password=self.password, name="TTest Bame"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password=self.password, name="Test User"
        )

    def tearDown(self):
        self.client = None
        self.admin_user.delete()
        self.user.delete()

    def test_authors_list_page(self):
        """Test that list page is working."""
        url = reverse("admin:blog_author_changelist")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_authors_edit_page(self):
        """Test that edit page is working."""
        author = Author.objects.create(
            user=self.user, first_name="Test", last_name="McTest"
        )
        url = reverse("admin:blog_author_change", args=[author.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_authors_create_page(self):
        """Test that creation page is working."""
        url = reverse("admin:blog_author_add")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_social_account_list_page(self):
        """Test that list page is working."""
        url = reverse("admin:blog_socialaccount_changelist")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_social_account_edit_page(self):
        """Test that edit page is working."""
        author = SocialAccount.objects.create(name="Twitter", url="twitter")
        url = reverse("admin:blog_socialaccount_change", args=[author.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_social_account_create_page(self):
        """Test that creation page is working."""
        url = reverse("admin:blog_socialaccount_add")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_post_list_page(self):
        """Test that list page is working."""
        url = reverse("admin:blog_post_changelist")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_post_edit_page(self):
        """Test that edit page is working."""
        obj = Post.objects.create(title="Title", content="Content")
        url = reverse("admin:blog_post_change", args=[obj.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_post_create_page(self):
        """Test that creation page is working."""
        url = reverse("admin:blog_post_add")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_category_list_page(self):
        """Test that list page is working."""
        url = reverse("admin:blog_category_changelist")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_category_edit_page(self):
        """Test that edit page is working."""
        obj = Category.objects.create(name="category")
        url = reverse("admin:blog_category_change", args=[obj.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_category_create_page(self):
        """Test that creation page is working."""
        url = reverse("admin:blog_category_add")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_tag_list_page(self):
        """Test that list page is working."""
        url = reverse("admin:blog_tag_changelist")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_tag_edit_page(self):
        """Test that edit page is working."""
        tag = Tag.objects.create(name="Angel")
        url = reverse("admin:blog_tag_change", args=[tag.id])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_tag_create_page(self):
        """Test that creation page is working."""
        url = reverse("admin:blog_tag_add")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
