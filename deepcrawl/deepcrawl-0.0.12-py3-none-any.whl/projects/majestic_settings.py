"""
Majestic Settings
=================
"""

from deepcrawl.utils import ImmutableAttributesMixin

majestic_mutable_fields = (
    'enabled',
    'max_rows',
    'use_historic_data',
    'use_root_domain'
)

majestic_immutable_fields = (
    '_project_href',
    '_href'
)

majestic_fields = majestic_mutable_fields + majestic_immutable_fields


class MajesticSettings(ImmutableAttributesMixin):
    """
    Majestic settings class
    """
    __slots__ = majestic_fields

    mutable_attributes = majestic_mutable_fields

    def __init__(self, majestic_settings):
        self.enabled = majestic_settings.get("enabled")
        self.max_rows = majestic_settings.get("max_rows")
        self.use_historic_data = majestic_settings.get("use_historic_data")
        self.use_root_domain = majestic_settings.get("use_root_domain")

        self._project_href = majestic_settings.get("_project_href")
        self._href = majestic_settings.get("_href")

        super(MajesticSettings, self).__init__()

    @property
    def to_dict_mutable_fields(self):
        return {x: getattr(self, x, None) for x in majestic_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        return {x: getattr(self, x, None) for x in majestic_immutable_fields}
