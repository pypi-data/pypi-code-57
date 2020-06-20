# Imports from Django.
from django.contrib import admin


# Imports from election.
from election.admin.utils import customTitledFilter
from election.models.election_type import ElectionType


PRIMARY_TYPE = ElectionType.PARTISAN_PRIMARY


class ElectionBallotAdmin(admin.ModelAdmin):
    autocomplete_fields = ["election_event"]
    list_display = (
        "get_election_event_name",
        "get_election_date",
        "get_election_type",
        "get_party",
        "get_offices_elected",
    )
    list_filter = (
        (
            "election_event__election_day__date",
            customTitledFilter("election date"),
        ),
        (
            "election_event__election_type__label",
            customTitledFilter("election type"),
        ),
        ("party__label", customTitledFilter("party")),
        ("offices_elected", customTitledFilter("offices being elected")),
    )
    list_select_related = (
        "election_event",
        "election_event__division",
        "election_event__election_day",
        "election_event__election_type",
        "party",
        # "election_ballot__election_event",
        # "election_ballot__election_event__election_day",
        # "election_ballot__election_event__election_type",
        # "race",
        # "race__office",
    )
    ordering = [
        "election_event__election_day__date",
        "election_event__division__slug",
        "election_event__election_type__label",
        "party__label",
    ]
    readonly_fields = ("uid", "slug")
    search_fields = (
        "election_event__division__name",
        "election_event__election_day__date",
        "election_event__election_day__slug",
        "election_event__election_type__slug",
        "election_event__notes",
        "overall_notes",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "election_event",
                    "party",
                    "offices_elected",
                    "overall_notes",
                )
            },
        ),
        (
            "Voter registration",
            {
                "fields": (
                    "online_registration_deadline",
                    "registration_deadline",
                    "registration_notes",
                )
            },
        ),
        (
            "Early voting",
            {
                "fields": (
                    "early_vote_start",
                    "early_vote_close",
                    "early_voting_notes",
                )
            },
        ),
        (
            "Voting by mail",
            {
                "fields": (
                    "vote_by_mail_application_deadline",
                    "vote_by_mail_ballot_deadline",
                )
            },
        ),
        (
            "Primary openness",
            {
                "fields": (
                    "who_can_vote",
                    "voters_register_by_party",
                    "party_reaffiliation_deadline_independent_voters",
                    "party_reaffiliation_deadline_other_party_voters",
                    "voting_reaffiliates_automatically",
                )
            },
        ),
        ("Election day information", {"fields": ("poll_closing_time",)}),
        ("Record locators", {"fields": ("uid", "slug")}),
    )

    def get_queryset(self, request):
        return (
            super(ElectionBallotAdmin, self)
            .get_queryset(request)
            .select_related(
                "election_event",
                "election_event__division",
                "election_event__election_day",
                "election_event__election_type",
                "party",
            )
        )

    def get_election_event_name(self, obj):
        return " ".join(
            [
                f"{obj.election_event.division_label}",
                f"{obj.election_event.election_type.get_slug_display()}",
            ]
        )

    get_election_event_name.short_description = "Election event"
    get_election_event_name.admin_order_field = (
        "election_event__division__slug"
    )

    def get_election_date(self, obj):
        return obj.election_event.election_day.date

    get_election_date.short_description = "Election date"
    get_election_date.admin_order_field = "election_event__election_day__date"

    def get_election_type(self, obj):
        return obj.election_event.election_type.label

    get_election_type.short_description = "Election Type"
    get_election_type.admin_order_field = (
        "election_event__election_type__label"
    )

    def get_party(self, obj):
        if obj.party:
            return obj.party.label
        else:
            return None

    get_party.short_description = "Primary Party"
    get_party.admin_order_field = "party__label"

    def get_offices_elected(self, obj):
        return obj.offices_elected

    get_offices_elected.short_description = "Offices being elected"
