from django.contrib.syndication.views import Feed
from django.urls import reverse
from customers.models import Customer

class NewsFeed(Feed):
    title = "News."
    link = "/news/"
    description = "Updates on changes and additions of the situation."

    def items(self):
        return Customer.objects.order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('news-item', args=[item.pk])