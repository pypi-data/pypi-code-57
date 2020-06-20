# Imports from Django.
from django.contrib import admin
from django import forms


# Imports from election.
from election.admin.utils import customTitledFilter
from election.models import Candidate
from election.models import CandidateElection
from election.models import ElectionBallot


class CandidateChoicesFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CandidateChoicesFormSet, self).__init__(*args, **kwargs)

        candidate_filter_kwargs = {}

        if self.instance.pk is not None:
            candidate_filter_kwargs = dict(
                cycle_id=self.instance.race.cycle_id,
                office_id=self.instance.race.office_id,
            )

            if self.instance.election_ballot.party_id is not None:
                candidate_filter_kwargs[
                    "party_id"
                ] = self.instance.election_ballot.party_id

        self.candidate_choices = list(
            Candidate.objects.filter(**candidate_filter_kwargs).values_list(
                "id", "uid"
            )
        )

    def get_form_kwargs(self, index):
        initial_kwargs = super(CandidateChoicesFormSet, self).get_form_kwargs(
            index
        )
        return {**initial_kwargs, "candidate_choices": self.candidate_choices}


class CandidateElectionInlineForm(forms.ModelForm):
    class Meta:
        model = CandidateElection
        fields = [
            "candidate",
            "ap_candidate_number",
            "ballot_order",
            "aggregable",
            "uncontested",
        ]

    def __init__(self, *args, **kwargs):
        candidate_choices = kwargs.pop("candidate_choices", [((), ())])
        super(CandidateElectionInlineForm, self).__init__(*args, **kwargs)

        self.fields["candidate"].choices = [("-", "---")] + candidate_choices
        self.fields["candidate"].initial = self.fields["candidate"].choices[0][
            0
        ]
        self.fields["candidate"].empty_values = (
            self.fields["candidate"].choices[0][0],
        )


class CandidateElectionInline(admin.StackedInline):
    form = CandidateElectionInlineForm
    formset = CandidateChoicesFormSet
    model = CandidateElection
    extra = 0

    def get_queryset(self, request):
        return (
            super(CandidateElectionInline, self)
            .get_queryset(request)
            .select_related("candidate")
        )


class ElectionAdminForm(forms.ModelForm):
    election_ballot = forms.ModelChoiceField(
        queryset=ElectionBallot.objects.all().select_related(
            "election_event",
            "election_event__division",
            "election_event__election_day",
            "election_event__election_type",
            "party",
            "party__organization",
        )
    )


class ElectionAdmin(admin.ModelAdmin):
    form = ElectionAdminForm
    list_display = (
        "get_office",
        "get_election_date",
        "get_election_type",
        "get_party",
        "get_special_status",
    )
    list_filter = (
        (
            "election_ballot__election_event__election_day__date",
            customTitledFilter("election date"),
        ),
        ("race__special", customTitledFilter("special election status")),
        (
            "election_ballot__election_event__election_type__label",
            customTitledFilter("election type"),
        ),
        ("election_ballot__party__label", customTitledFilter("party")),
    )
    list_select_related = (
        "election_ballot",
        "election_ballot__election_event",
        "election_ballot__election_event__election_day",
        "election_ballot__election_event__election_type",
        "race",
        "race__office",
    )
    ordering = (
        "election_ballot__election_event__election_day__date",
        "election_ballot__election_event__division__label",
        "race__office__label",
        "election_ballot__party__label",
    )
    search_fields = (
        "race__label",
        "ap_election_id",
        "election_ballot__election_event__election_day__date",
        "election_ballot__election_event__election_day__slug",
        "election_ballot__election_event__notes",
        "election_ballot__overall_notes",
    )
    autocomplete_fields = ["race"]
    inlines = [CandidateElectionInline]
    readonly_fields = ("uid",)
    fieldsets = (
        (
            "Relationships",
            {
                "fields": (
                    "election_ballot",
                    "race",
                    "ap_election_id",
                    "race_type_slug",
                    "national_delegates_awarded",
                )
            },
        ),
        ("Record locators", {"fields": ("uid",)}),
    )

    def get_queryset(self, request):
        return (
            super(ElectionAdmin, self)
            .get_queryset(request)
            .select_related(
                "election_ballot",
                "election_ballot__election_event",
                "election_ballot__election_event__division",
                "election_ballot__election_event__election_day",
                "election_ballot__election_event__election_type",
                "election_ballot__party",
                "race",
                "race__office",
            )
        )

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []

        return [inline(self.model, self.admin_site) for inline in self.inlines]

    def get_office(self, obj):
        if obj.race.office.label.lower() == "u.s. president":
            division_label = obj.election_ballot.election_event.division.label
            return f"{obj.race.office.label} — {division_label}"

        return obj.race.office.label

    get_office.short_description = "Office"
    get_office.admin_order_field = "race__office__label"

    def get_election_date(self, obj):
        return obj.election_ballot.election_event.election_day.date

    get_election_date.short_description = "Election date"
    get_election_date.admin_order_field = (
        "election_ballot__election_event__election_day__date"
    )

    def get_election_type(self, obj):
        return obj.election_ballot.election_event.election_type.label

    get_election_type.short_description = "Election Type"
    get_election_type.admin_order_field = (
        "election_ballot__election_event__election_type__label"
    )

    def get_party(self, obj):
        if obj.election_ballot.party:
            return obj.election_ballot.party.label
        else:
            return None

    get_party.short_description = "Primary Party"
    get_party.admin_order_field = "election_ballot__party__label"

    def get_special_status(self, obj):
        return obj.race.special

    get_special_status.short_description = "Is special?"
    get_special_status.boolean = True
    get_special_status.admin_order_field = "race__special"
