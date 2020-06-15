from django_filters import FilterSet, filters

from whisperer.models import Webhook, WebhookEvent


class WebhookFilter(FilterSet):
    target_url = filters.CharFilter(field_name="target_url", lookup_expr="iexact")

    class Meta:
        model = Webhook
        fields = ('target_url', 'is_active', 'event_type')


class WebhookEventFilter(FilterSet):
    event_type = filters.CharFilter(
        field_name='webhook__event_type', lookup_expr='iexact'
    )
    created_date = filters.DateFilter(field_name='created_date', lookup_expr='__all__')

    class Meta:
        model = WebhookEvent
        fields = (
            'uuid',
            'event_type',
            'response_http_status',
            'delivered',
            'created_date',
        )
