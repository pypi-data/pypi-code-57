import collections
import itertools
import re
from typing import Iterable

from ._model import CATEGORIES, SEVERITIES, Patch, Product

GAUGE_META_TEMPLATE = '''\
# HELP {name} {help_text}
# TYPE {name} gauge
'''


GAUGE_VALUE_TEMPLATE = '''\
{name} {value}
'''


def _render_gauge_meta(name, help_text):
    return GAUGE_META_TEMPLATE.format(
        name=name,
        help_text=help_text
    )


def _render_gauge_value(name, value):
    return GAUGE_VALUE_TEMPLATE.format(
        name=name,
        value=value,
    )


def _render_patch_meta():
    return _render_gauge_meta(
        name='zypper_applicable_patches',
        help_text='The current count of applicable patches',
    )


def _render_patch_count(patch, count):
    return _render_gauge_value(
        name='zypper_applicable_patches{{category="{category}",severity="{severity}"}}'.format(
            category=patch.category,
            severity=patch.severity,
        ),
        value=count,
    )


def _render_service_needs_restart_meta():
    return _render_gauge_meta(
        name='zypper_service_needs_restart',
        help_text='Set to 1 if service requires a restart due to using no-longer-existing libraries.',
    )


def _render_service_needs_restart_value(service: str):
    # There is only a specific set of characters allowed in labels.
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', service)

    return _render_gauge_value(
        name=f'zypper_service_needs_restart{{service="{safe_name}"}}',
        value=1,
    )


def _render_product_meta():
    return _render_gauge_meta(
        name='zypper_product_end_of_life',
        help_text='Unix timestamp on when support for the product will end.',
    )


def _render_product_eol(product: Product):
    # There is only a specific set of characters allowed in labels.
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', product.name)

    return _render_gauge_value(
        name=f'zypper_product_end_of_life{{product="{safe_name}"}}',
        value=product.eol,
    )


def _render_needs_rebooting(needs_rebooting):
    return _render_gauge_meta(
        name='zypper_needs_rebooting',
        help_text='Whether the system requires a reboot as core libraries or services have been updated.',
    ) + _render_gauge_value(
        name='zypper_needs_rebooting',
        value=1 if needs_rebooting else 0
    )


def _render_scrape_success(value):
    return _render_gauge_meta(
        name='zypper_scrape_success',
        help_text='Whether the last scrape for zypper data was successful.',
    ) + _render_gauge_value(
        name='zypper_scrape_success',
        value=value,
    )


def render(
    patches: Iterable[Patch],
    services_needing_restart: Iterable[str],
    needs_rebooting: bool,
    products: Iterable[Product],
):
    patch_histogram = collections.Counter(patches)

    if patches is None or services_needing_restart is None or products is None:
        return _render_scrape_success(0)

    metrics = [
        _render_patch_meta()
    ] + [
        _render_patch_count(patch, patch_histogram.get(patch, 0))
        for patch in (
            Patch(category, severity) for category, severity in itertools.product(CATEGORIES, SEVERITIES)
        )
    ] + [
        _render_service_needs_restart_meta()
    ] + [
        _render_service_needs_restart_value(service) for service in services_needing_restart
    ] + [
        _render_product_meta()
    ] + [
        _render_product_eol(product) for product in products
    ] + [
        _render_needs_rebooting(needs_rebooting),
        _render_scrape_success(1)
    ]
    return ''.join(metrics)
