import datetime
from wagtail.core import hooks
from wagtail.admin.site_summary import SummaryItem
from lionclaw.orders.models import Order
from lionclaw.stats import stats
from lionclaw.configuration.models import Configuration
from lionclaw.utils import ProductVariant, maybe_get_product_model
from django.utils.translation import ugettext_lazy as _

class LionclawSummaryItem(SummaryItem):
    order = 10
    template = 'stats/summary_item.html'

    def get_context(self):
        return {
            'total': 0,
            'text': '',
            'url': '',
            'icon': 'icon-doc-empty-inverse'
        }

class OutstandingOrders(LionclawSummaryItem):
    order = 10
    def get_context(self):
        orders = Order.objects.filter(status=Order.SUBMITTED)
        return {
            'total': orders.count(),
            'text': 'Outstanding Orders',
            'url': '/admin/orders/order/',
            'icon': 'icon-warning'
        }

class ProductCount(LionclawSummaryItem):
    order = 20
    def get_context(self):
        product_model = maybe_get_product_model()
        if product_model:
            count = product_model.objects.all().count()
        else:
            count = ProductVariant.objects.all().count()
        return {
            'total': count,
            'text': _('Product'),
            'url': '',
            'icon': 'icon-list-ul'
        }

class MonthlySales(LionclawSummaryItem):
    order = 30
    def get_context(self):
        settings = Configuration.for_site(self.request.site)
        sales = stats.sales_for_time_period(*stats.current_month())
        return {
            'total': "{}{}".format(settings.currency_html_code,
                                   sum(order.total for order in sales)),
            'text': _('In sales this month'),
            'url': '/admin/orders/order/',
            'icon': 'icon-tick'
        }

class LionclawStatsPanel(SummaryItem):
    order = 110
    template = 'stats/stats_panel.html'
    def get_context(self):
        month_start, month_end = stats.current_month()
        daily_sales = stats.daily_sales(month_start, month_end)
        labels = [(month_start + datetime.timedelta(days=x)).strftime('%d-%m-%Y')
                  for x in range(0, datetime.datetime.now().day)]
        daily_income = [0] * len(labels)
        for k, order_group in daily_sales:
            i = labels.index(k)
            daily_income[i] = float(sum(order.total for order in order_group))

        popular_products = stats.sales_by_product(month_start, month_end)[:5]
        return {
            "daily_income": daily_income,
            "labels": labels,
            "product_labels": list(popular_products.values_list('title', flat=True)),
            "sales_volume": list(popular_products.values_list('quantity', flat=True))
        }




@hooks.register('construct_homepage_summary_items')
def add_lionclaw_summary_items(request, items):

    # We are going to replace everything with our own items
    items[:] = []
    items.extend([
        OutstandingOrders(request),
        ProductCount(request),
        MonthlySales(request)
    ])

@hooks.register('construct_homepage_panels')
def add_stats_panel(request, panels):
    return panels.append(LionclawStatsPanel(request))
