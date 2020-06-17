from django.conf.urls import url
from lionclaw.orders import api

from lionclaw.settings import API_URL_PREFIX

orders = api.OrderViewSet.as_view({
    'get': 'retrieve'
})

fulfill_order = api.OrderViewSet.as_view({
    'post': 'fulfill_order'
})

refund_order = api.OrderViewSet.as_view({
    'post': 'refund_order'
})

PREFIX = r'^{}order/'.format(API_URL_PREFIX)
urlpatterns = [
    url(
        PREFIX + r'(?P<pk>[0-9]+)/$',
        orders,
        name='lionclaw_orders'
    ),

    url(
        PREFIX + r'(?P<pk>[0-9]+)/fulfill/$',
        fulfill_order,
        name='lionclaw_fulfill_order'
    ),

    url(
        PREFIX + r'(?P<pk>[0-9]+)/refund/$',
        refund_order,
        name='lionclaw_refund_order'
    )
]
