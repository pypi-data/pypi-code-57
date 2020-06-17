import re

import pytest

from zypper_patch_status_collector._model import CATEGORIES, SEVERITIES, Patch, Product
from zypper_patch_status_collector._prometheus import render

# Expect all category-severity combinations and the zypper query failed metric
EXPECTED_METRICS_COUNT = len(CATEGORIES) * len(SEVERITIES) + 2


def _parse_metrics(metrics):
    parsed = {}

    for line in metrics.splitlines():
        metric_match = re.match(r'^(?P<metric>\S+)\s+(?P<value>\S+)$', line)
        if metric_match:
            parsed[metric_match.group('metric')] = float(metric_match.group('value'))

    return parsed


def test_render_no_patches():
    patches = []

    metrics = render(patches, [], False, [])

    parsed_metrics = _parse_metrics(metrics)
    assert len(parsed_metrics) == EXPECTED_METRICS_COUNT
    assert parsed_metrics.pop('zypper_scrape_success') == 1
    for value in parsed_metrics.values():
        assert value == 0


def test_render_multiple_patches():
    patches = [
        Patch('security', 'important'),
        Patch('optional', 'moderate'),
        Patch('security', 'important'),
    ]

    metrics = render(patches, [], False, [])

    parsed_metrics = _parse_metrics(metrics)
    assert len(parsed_metrics) == EXPECTED_METRICS_COUNT
    assert parsed_metrics['zypper_applicable_patches{category="security",severity="important"}'] == 2
    assert parsed_metrics['zypper_applicable_patches{category="optional",severity="moderate"}'] == 1
    assert parsed_metrics['zypper_applicable_patches{category="feature",severity="low"}'] == 0
    assert parsed_metrics['zypper_scrape_success'] == 1


@pytest.mark.parametrize('needs_reboot,expected', [
    (True, 1),
    (False, 0),
])
def test_render_needs_rebooting(needs_reboot, expected):
    assert _parse_metrics(render([], [], needs_reboot, []))['zypper_needs_rebooting'] == expected


def test_render_lifecycle():
    products = [
        Product('openSUSE', 12),
        Product('something else', 9)
    ]

    metrics = render([], [], False, products)

    parsed_metrics = _parse_metrics(metrics)
    assert len(parsed_metrics) == EXPECTED_METRICS_COUNT + len(products)
    assert parsed_metrics['zypper_product_end_of_life{product="openSUSE"}'] == 12
    assert parsed_metrics['zypper_product_end_of_life{product="something_else"}'] == 9


def test_render_services_needing_restart():
    services = ['apache', 'mysql']

    metrics = render([], services, False, [])

    parsed_metrics = _parse_metrics(metrics)
    assert len(parsed_metrics) == EXPECTED_METRICS_COUNT + len(services)
    assert parsed_metrics['zypper_service_needs_restart{service="apache"}'] == 1
    assert parsed_metrics['zypper_service_needs_restart{service="mysql"}'] == 1


def test_render_failure():
    patches = None
    products = None
    services = None

    metrics = render(patches, services, False, products)

    parsed_metrics = _parse_metrics(metrics)
    assert len(parsed_metrics) == 1
    assert parsed_metrics['zypper_scrape_success'] == 0
