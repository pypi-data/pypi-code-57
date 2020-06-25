"""
Report
======
"""

import deepcrawl
from deepcrawl.utils import ImmutableAttributesMixin

report_extra_fields = (
    'id',
    'account_id',
    'project_id',
    'crawl_id',
    'report_rows',
)

report_mutable_fields = report_extra_fields + (
    'report_type',
    'report_template',
    'total_rows',
    'basic_total',
    'removed_total',
    'added_total',
    'missing_total',
    'change_weight',
    'total_weight',
    'beta',
)

report_immutable_fields = (
    '_datasource_href',
    '_report_template_href',
    '_recent_report_trend_href',
    '_account_href',
    '_project_href',
    '_crawl_href',
    '_report_type_href',
    '_href',
    '_href_alt',
    '_report_downloads_href',
    '_report_rows_href',
    '_statistics_href',
    '_issues_href',
    '_added_report_href',
    '_added_report_href_alt',
    '_basic_report_href',
    '_basic_report_href_alt',
    '_missing_report_href',
    '_missing_report_href_alt',
)

report_fields = report_mutable_fields + report_immutable_fields


class DeepCrawlReport(ImmutableAttributesMixin):
    """
    Report class
    """
    __slots__ = report_fields

    mutable_attributes = report_mutable_fields

    def __init__(self, account_id, project_id, crawl_id, report_data: dict):
        # relations
        self.id = report_data.get("id")
        self.account_id = account_id
        self.project_id = project_id
        self.crawl_id = crawl_id
        self.report_rows = []

        # attributes
        self.report_type = report_data.get('report_type')
        self.report_template = report_data.get('report_template')
        self.total_rows = report_data.get('total_rows')
        self.basic_total = report_data.get('basic_total')
        self.removed_total = report_data.get('removed_total')
        self.added_total = report_data.get('added_total')
        self.missing_total = report_data.get('missing_total')
        self.change_weight = report_data.get('change_weight')
        self.total_weight = report_data.get('total_weight')
        self.beta = report_data.get('beta')

        self._datasource_href = report_data.get('_datasource_href')
        self._report_template_href = report_data.get('_report_template_href')
        self._recent_report_trend_href = report_data.get('_recent_report_trend_href')
        self._account_href = report_data.get('_account_href')
        self._project_href = report_data.get('_project_href')
        self._crawl_href = report_data.get('_crawl_href')
        self._report_type_href = report_data.get('_report_type_href')
        self._href = report_data.get('_href')
        self._href_alt = report_data.get('_href_alt')
        self._report_downloads_href = report_data.get('_report_downloads_href')
        self._report_rows_href = report_data.get('_report_rows_href')
        self._statistics_href = report_data.get('_statistics_href')
        self._issues_href = report_data.get('_issues_href')
        self._added_report_href = report_data.get('_added_report_href')
        self._added_report_href_alt = report_data.get('_added_report_href_alt')
        self._basic_report_href = report_data.get('_basic_report_href')
        self._basic_report_href_alt = report_data.get('_basic_report_href_alt')
        self._missing_report_href = report_data.get('_missing_report_href')
        self._missing_report_href_alt = report_data.get('_missing_report_href_alt')

        super(DeepCrawlReport, self).__init__()

    def __repr__(self):
        return f"[{self.account_id} {self.project_id} {self.crawl_id}] {self.id}"

    def __str__(self):
        return f"[{self.account_id} {self.project_id} {self.crawl_id}] {self.id}"

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in report_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in report_immutable_fields}

    def load_report_rows(self, connection=None, filters=None, **kwargs):
        """Loads reports rows into current instance

        >>> self.load_report_rows()
        [<deepcrawl.reports.report_row.DeepCrawlReportRow at 0x108a20600>,
        <deepcrawl.reports.report_row.DeepCrawlReportRow at 0x148a25670>]
        >>> self.report_rows
        [<deepcrawl.reports.report_row.DeepCrawlReportRow at 0x108a20600>,
        <deepcrawl.reports.report_row.DeepCrawlReportRow at 0x148a25670>]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of report rows
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.report_rows = connection.get_report_rows(
            self.account_id, self.project_id, self.crawl_id, self.id, filters=filters, **kwargs
        )
        return self.report_rows

    def get_report_row(self, report_row_id, connection=None):
        """Get report row

        >>> self.get_report_row(1)
        <deepcrawl.reports.report_row.DeepCrawlReportRow at 0x108a20600>

        :param report_row_id: report row id
        :type report_row_id: int
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: report row instance
        :rtype: DeepCrawlReportRow
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_report_row(self.account_id, self.project_id, self.crawl_id, self.id, report_row_id)

    def get_report_rows(self, use_cache=True, connection=None, filters=None, **kwargs):
        """Get report rows for current instance

        * use_cache=True > get_report_rows will return cached report rows or will do a call to DeepCrawl if report_rows attribute is empty.
        * use_cache=False > get_report_rows will call DeepCrawl api and will override report_rows attribute.

        >>> self.get_report_rows()
        [<deepcrawl.reports.report_row.DeepCrawlReportRow at 0x108a20600>,
        <deepcrawl.reports.report_row.DeepCrawlReportRow at 0x148a25670>]

        :param use_cache:
        :type use_cache: bool
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: List of report rows
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if self.report_rows and use_cache:
            return self.report_rows
        return self.load_report_rows(connection=connection, filters=filters, **kwargs)

    def get_report_row_count(self, connection=None, filters=None):
        """Get report row count

        >>> connection.get_report_row_count()
        "2"

        :param filters: filters dict
        :type filters: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: Count of report row
        :rtype: str
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_report_row_count(
            self.account_id, self.project_id, self.crawl_id, self.id, filters=filters
        )
