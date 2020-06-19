from coldcms.blog.models import (
    BlogAuthorIndexPage,
    BlogDateIndexPage,
    BlogIndexPage,
    BlogListAuthorsIndexPage,
    BlogListDatesIndexPage,
    BlogListTagsIndexPage,
    BlogPage,
    BlogTagIndexPage,
)
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _


def refresh_tags():
    used_tags = set()
    for blog_page in BlogPage.objects.all().live():
        used_tags.update(tag for tag in blog_page.tags.all())

    existing_tag_index_pages = {
        blog_tag_index.tag for blog_tag_index in BlogTagIndexPage.objects.all()
    }

    tags_to_remove = existing_tag_index_pages - used_tags
    tags_to_add = used_tags - existing_tag_index_pages

    BlogTagIndexPage.objects.filter(tag__in=tags_to_remove).delete()

    parent_page = BlogListTagsIndexPage.objects.first()
    if not parent_page:
        parent_page = BlogListTagsIndexPage(
            title=_("Tags"), slug="tags", show_in_menus=False
        )
        blog = BlogIndexPage.objects.first()
        blog.add_child(instance=parent_page)
        parent_page.save_revision().publish()

    for tag in tags_to_add:
        new_index_page = BlogTagIndexPage(
            title=_("Blog posts tagged '%(tag)s'") % {"tag": tag.name},
            tag=tag,
            slug=slugify(tag.name),
        )
        parent_page.add_child(instance=new_index_page)
        new_index_page.save_revision().publish()


def refresh_authors():
    existing_users = {blog_page.owner for blog_page in BlogPage.objects.all().live()}
    existing_author_index_pages = {
        blog_author_index.author
        for blog_author_index in BlogAuthorIndexPage.objects.all()
    }

    authors_to_remove = existing_author_index_pages - existing_users
    authors_to_add = existing_users - existing_author_index_pages

    BlogAuthorIndexPage.objects.filter(author__in=authors_to_remove).delete()

    parent_page = BlogListAuthorsIndexPage.objects.first()
    if not parent_page:
        parent_page = BlogListAuthorsIndexPage(
            title=_("Authors"), slug="authors", show_in_menus=False
        )
        blog = BlogIndexPage.objects.first()
        blog.add_child(instance=parent_page)
        parent_page.save_revision().publish()

    for author in authors_to_add:
        new_index_page = BlogAuthorIndexPage(
            title=_("Blog posts by %(author)s") % {"author": author.username.title()},
            author=author,
            slug=slugify(author.username),
        )
        parent_page.add_child(instance=new_index_page)
        new_index_page.save_revision().publish()


def refresh_dates():
    existing_dates = {
        blog_page.date.replace(day=1) for blog_page in BlogPage.objects.all().live()
    }
    existing_date_index_pages = {
        blog_date_index.date.replace(day=1)
        for blog_date_index in BlogDateIndexPage.objects.all()
    }

    dates_to_remove = existing_date_index_pages - existing_dates
    dates_to_add = existing_dates - existing_date_index_pages

    BlogDateIndexPage.objects.filter(date__in=dates_to_remove).delete()

    parent_page = BlogListDatesIndexPage.objects.first()
    if not parent_page:
        parent_page = BlogListDatesIndexPage(
            title=_("Dates"), slug="dates", show_in_menus=False
        )
        blog = BlogIndexPage.objects.first()
        blog.add_child(instance=parent_page)
        parent_page.save_revision().publish()

    for date in dates_to_add:
        new_index_page = BlogDateIndexPage(
            title=_("Blog posts published on %(date)s")
            % {"date": date.strftime("%B, %Y")},
            date=date,
            slug=slugify(date.strftime("%B-%Y")),
        )

        parent_page.add_child(instance=new_index_page)
        new_index_page.save_revision().publish()


def refresh_index_pages(sender=None, instance=None, revision=None, **kwargs):
    if sender != BlogPage:
        return

    refresh_tags()
    refresh_authors()
    refresh_dates()
