# Imports from Django.
from django.contrib import admin


# Imports from election.
from election.admin.utils import customTitledFilter
from election.models.election_data_url import ElectionDataURL
from election.models.election_type import ElectionType


PRIMARY_TYPE = ElectionType.PARTISAN_PRIMARY


class ElectionDataURLInline(admin.TabularInline):
    model = ElectionDataURL

    def get_queryset(self, request):
        return (
            super(ElectionDataURLInline, self)
            .get_queryset(request)
            .select_related(
                "election_event",
                "election_event__division",
                "election_event__election_day",
                "election_event__election_type",
            )
        )


class ElectionEventAdmin(admin.ModelAdmin):
    list_display = (
        "get_election_event_name",
        "get_election_date",
        "get_election_mode",
        "get_election_url_count",
    )
    list_filter = (
        ("election_day__date", customTitledFilter("election date")),
        ("election_type__label", customTitledFilter("election type")),
        ("election_mode", customTitledFilter("status")),
    )
    list_select_related = ("division", "election_day", "election_type")
    fields = [
        "division",
        "election_day",
        "election_type",
        "election_mode",
        "notes",
    ]
    inlines = [ElectionDataURLInline]
    ordering = ["election_day__date", "division__slug", "election_type__label"]
    readonly_fields = ("uid", "slug")
    search_fields = (
        "division__name",
        "election_day__date",
        "election_day__slug",
        "election_type__slug",
        "notes",
    )

    def get_queryset(self, request):
        return (
            super(ElectionEventAdmin, self)
            .get_queryset(request)
            .select_related("division", "election_day", "election_type")
            .prefetch_related("data_urls")
        )

    def get_election_event_name(self, obj):
        return " ".join(
            [
                f"{obj.division_label}",
                f"{obj.election_type.get_slug_display()}",
            ]
        )

    get_election_event_name.short_description = "Election event"
    get_election_event_name.admin_order_field = "division__slug"

    def get_election_date(self, obj):
        return obj.election_day.date

    get_election_date.short_description = "Election date"
    get_election_date.admin_order_field = "election_day__date"

    def get_election_mode(self, obj):
        return obj.get_election_mode_display()

    get_election_mode.short_description = "Status"
    get_election_mode.admin_order_field = "election_mode"

    def get_election_url_count(self, obj):
        return obj.data_urls.count()

    get_election_url_count.short_description = "Configured URLs"
