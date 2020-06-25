"""
Extractions
===========
"""

from deepcrawl.utils import ImmutableAttributesMixin

extraction_mutable_fields = (
    'label',
    'regex',
    'match_number_from',
    'match_number_to',
    'filter',
    'clean_html_tags'
)

extraction_immutable_fields = (

)


extraction_fields = extraction_mutable_fields + extraction_immutable_fields


class DeepCrawlExtraction(ImmutableAttributesMixin):
    """
    Extractions class
    """
    __slots__ = extraction_fields

    mutable_attributes = extraction_mutable_fields

    def __init__(self, extraction_data):
        self.label = extraction_data.get('label')
        self.regex = extraction_data.get('regex')
        self.match_number_from = extraction_data.get('match_number_from')
        self.match_number_to = extraction_data.get('match_number_to')
        self.filter = extraction_data.get('filter', '')
        self.clean_html_tags = extraction_data.get('clean_html_tags', False)

        super(DeepCrawlExtraction, self).__init__()

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in extraction_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in extraction_immutable_fields}
