from django.conf.urls import include, url
from lionclaw.basket import urls as basket_urls
from lionclaw.checkout import urls as checkout_urls
from lionclaw.shipping import urls as shipping_urls
from lionclaw.orders import urls as order_urls

urlpatterns = [
    url(r'', include(basket_urls)),
    url(r'', include(checkout_urls)),
    url(r'', include(shipping_urls)),
    url(r'', include(order_urls)),
]
