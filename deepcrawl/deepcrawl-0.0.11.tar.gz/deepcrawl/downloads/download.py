"""
Download
========
"""

from deepcrawl.utils import ImmutableAttributesMixin
from deepcrawl.utils import safe_string_to_datetime

crawl_download_extra_fields = (
    'id',
    'account_id',
    'project_id',
    'crawl_id',
    'report_id',
)

crawl_download_mutable_fields = crawl_download_extra_fields + (
    'report_type',
    'status',
    'date_requested',
    'total_rows',
    'report_file',
    'report_name',
    'filter',
    'output_type',
)

crawl_download_immutable_fields = (
    '_account_href',
    '_project_href',
    '_crawl_href',
    '_report_href',
    '_report_href_alt',
    '_report_template_href',
    '_report_type_href',
    '_href',
)

crawl_download_fields = crawl_download_mutable_fields + crawl_download_immutable_fields


class DeepCrawlCrawlDownloads(ImmutableAttributesMixin):
    """
    Crawls Download class
    """
    __slots__ = crawl_download_fields

    mutable_attributes = crawl_download_mutable_fields

    def __init__(self, download_data, account_id, project_id, crawl_id):
        # relations
        self.account_id = account_id
        self.project_id = project_id
        self.crawl_id = crawl_id

        # attributes
        self.id = download_data.get('id')
        self.report_type = download_data.get('report_type')
        self.status = download_data.get('status')
        self.filter = download_data.get('filter')
        self.output_type = download_data.get('output_type')
        self.date_requested = safe_string_to_datetime(
            download_data.get('date_requested')
        )
        self.total_rows = download_data.get('total_rows')
        self.report_file = download_data.get('report_file')
        self._account_href = download_data.get('_account_href')
        self._project_href = download_data.get('_project_href')
        self._crawl_href = download_data.get('_crawl_href')
        self._report_href = download_data.get('_report_href')
        self._report_href_alt = download_data.get('_report_href_alt')
        self._report_template_href = download_data.get('_report_template_href')
        self._report_type_href = download_data.get('_report_type_href')
        self._href = download_data.get('_href')

        self.report_name = self._report_href_alt.split('/')[-1]

        super(DeepCrawlCrawlDownloads, self).__init__()

    def __repr__(self):
        return f"[{self.id}] {self.report_name.title()} {self.report_type} - {self.output_type} ({self.status})"

    def __str__(self):
        return f"[{self.id}] {self.report_name.title()} {self.report_type} - {self.output_type} ({self.status})"

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in crawl_download_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in crawl_download_immutable_fields}


report_download_extra_fields = (
    "id",
    "account_id",
    "project_id",
    "crawl_id",
    "report_id",
)

report_download_mutable_fields = report_download_extra_fields + (
    "report_type",
    "status",
    "filter",
    "output_type",
    "date_requested",
    "total_rows",
    "output_requested"
)

report_download_immutable_fields = (

)

report_download_fields = report_download_mutable_fields + report_download_immutable_fields


class DeepCrawlReportDownload(ImmutableAttributesMixin):
    """
    Reports Download class
    """

    __slots__ = report_download_fields

    mutable_attributes = report_download_mutable_fields

    def __init__(self, account_id, project_id, crawl_id, report_id, download_data: dict):
        # relations
        self.id = download_data.get("id")
        self.account_id = account_id
        self.project_id = project_id
        self.crawl_id = crawl_id
        self.report_id = report_id

        # attributes
        self.report_type = download_data.get('report_type')
        self.status = download_data.get('status')
        self.filter = download_data.get('filter')
        self.output_type = download_data.get('output_type')
        self.date_requested = safe_string_to_datetime(download_data.get('date_requested'))
        self.total_rows = download_data.get('total_rows')

        # only in create (I think.)
        self.output_requested = download_data.get('output_requested')

        super(DeepCrawlReportDownload, self).__init__()

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in report_download_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in report_download_immutable_fields}
