from django import forms


class OpeningHoursRelatedAdminMixin:
    @property
    def media(self):
        media = super().media + forms.Media(
            js=["admin/js/RelatedOpeningHoursLookups.js"]
        )
        return media
