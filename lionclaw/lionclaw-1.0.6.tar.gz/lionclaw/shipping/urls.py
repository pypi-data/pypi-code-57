from django.conf.urls import url
from lionclaw.shipping import api
from lionclaw.settings import API_URL_PREFIX

address_list = api.AddressViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
address_detail = api.AddressViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    url(API_URL_PREFIX + r'addresses/$',
        address_list,
        name='lionclaw_address_list'),
    url(API_URL_PREFIX + r'addresses/(?P<pk>[0-9]+)/$',
        address_detail,
        name='lionclaw_address_detail'),
    url(API_URL_PREFIX + r'shipping/cost/$',
        api.shipping_cost,
        name='lionclaw_shipping_cost'),
    url(API_URL_PREFIX + r'shipping/countries/$',
        api.shipping_countries,
        name='lionclaw_shipping_countries'),
    url(API_URL_PREFIX + r'shipping/countries/(?P<country>[a-zA-Z]+)/$',
        api.shipping_options,
        name='lionclaw_shipping_options'),
    url(API_URL_PREFIX + r'shipping/options/$',
        api.shipping_options,
        name='lionclaw_applicable_shipping_rate_list')
]
