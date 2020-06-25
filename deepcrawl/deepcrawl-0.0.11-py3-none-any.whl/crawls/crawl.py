"""
Crawl
=====
"""

import deepcrawl
from deepcrawl.utils import ImmutableAttributesMixin
from deepcrawl.utils import safe_string_to_datetime

crawl_extra_fields = (
    'id',
    'account_id',
    'project_id',
    'reports',
    'reports_changes',
    'downloads',
)

crawl_mutable_fields = crawl_extra_fields + (
    'crawling_at',
    'finished_at',
    'progress_crawled',
    'progress_enqueued',
    'progress_uncrawled',
    'progress_crawling',
    'progress_finalizing',
    'progress_overall',
    'stats_crawled',
    'crawl_types',
    'stats_crawl_levels',
    'status',
    'total_step_links',
    'total_steps',
    'v1_migration_status',
    'pause_reason',
    'crawl_rate_current_limit',
    'crawl_rate',
    'crawl_rate_advanced',
    'status_internal',
    'optimus_transformed',
    'unique_pages_total',
    'levels_total',
    'all_pages_total',
    'uncrawled_urls_total',
    'crawl_compare_to_finished_at',
    'crawl_compare_to_crawl_test_site',
    'crawled_s',
)

crawl_immutable_fields = (
    '_account_href',
    '_project_href',
    '_crawl_settings_last_href',
    '_href',
    '_reports_href',
    '_sitemaps_href',
    '_statistics_href',
    '_site_explorer_href',
    '_crawl_compare_to_href',
    '_changes_href',
)

crawl_fields = crawl_mutable_fields + crawl_immutable_fields


class DeepCrawlCrawl(ImmutableAttributesMixin):
    """
    Crawl class
    """
    __slots__ = crawl_fields

    mutable_attributes = crawl_mutable_fields

    def __init__(self, crawl_data, account_id, project_id):
        # relations
        self.id = crawl_data.get('id')
        self.account_id = account_id
        self.project_id = project_id
        self.reports = []
        self.reports_changes = []
        self.downloads = []

        # attributes
        self.crawling_at = safe_string_to_datetime(crawl_data.get('crawling_at'))
        self.finished_at = safe_string_to_datetime(crawl_data.get('finished_at'))
        self.progress_crawled = crawl_data.get('progress_crawled')
        self.progress_enqueued = crawl_data.get('progress_enqueued')
        self.progress_uncrawled = crawl_data.get('progress_uncrawled')
        self.progress_crawling = crawl_data.get('progress_crawling')
        self.progress_finalizing = crawl_data.get('progress_finalizing')
        self.progress_overall = crawl_data.get('progress_overall')
        self.stats_crawled = crawl_data.get('stats_crawled')
        self.crawl_types = crawl_data.get('crawl_types')
        self.stats_crawl_levels = crawl_data.get('stats_crawl_levels')
        self.status = crawl_data.get('status')
        self.total_step_links = crawl_data.get('total_step_links')
        self.total_steps = crawl_data.get('total_steps')
        self.v1_migration_status = crawl_data.get('v1_migration_status')
        self.pause_reason = crawl_data.get('pause_reason')
        self.crawl_rate_current_limit = crawl_data.get('crawl_rate_current_limit')
        self.crawl_rate = crawl_data.get('crawl_rate')
        self.crawl_rate_advanced = crawl_data.get('crawl_rate_advanced')
        self.status_internal = crawl_data.get('status_internal')
        self.optimus_transformed = crawl_data.get('optimus_transformed')
        self.unique_pages_total = crawl_data.get('unique_pages_total')
        self.levels_total = crawl_data.get('levels_total')
        self.all_pages_total = crawl_data.get('all_pages_total')
        self.uncrawled_urls_total = crawl_data.get('uncrawled_urls_total')
        self.crawl_compare_to_finished_at = safe_string_to_datetime(crawl_data.get('crawl_compare_to_finished_at'))
        self.crawl_compare_to_crawl_test_site = crawl_data.get('crawl_compare_to_crawl_test_site')
        self.crawled_s = crawl_data.get('crawled_/_s')

        self._account_href = crawl_data.get('_account_href')
        self._project_href = crawl_data.get('_project_href')
        self._crawl_settings_last_href = crawl_data.get('_crawl_settings_last_href')
        self._href = crawl_data.get('_href')
        self._reports_href = crawl_data.get('_reports_href')
        self._sitemaps_href = crawl_data.get('_sitemaps_href')
        self._statistics_href = crawl_data.get('_statistics_href')
        self._site_explorer_href = crawl_data.get('_site_explorer_href')
        self._crawl_compare_to_href = crawl_data.get('_crawl_compare_to_href')
        self._changes_href = crawl_data.get('_changes_href')

        super(DeepCrawlCrawl, self).__init__()

    def __repr__(self):
        return f"[{self.account_id} {self.project_id} {self.id}] {self.crawling_at}"

    def __str__(self):
        return f"[{self.account_id} {self.project_id} {self.id}] {self.crawling_at}"

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in crawl_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in crawl_immutable_fields}

    def load_reports(self, connection=None, filters=None, **kwargs):
        """Loads reports into current instance

        >>> self.load_reports()
        [[0 1 2] 4:duplicate_body_content:basic,
        [0 1 2] 4:duplicate_body_content:added]
        >>> self.reports
        [[0 1 2] 4:duplicate_body_content:basic,
        [0 1 2] 4:duplicate_body_content:added]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of reports
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.reports = connection.get_reports(self.account_id, self.project_id, self.id, filters=filters, **kwargs)
        return self.reports

    def load_reports_changes(self, connection=None, filters=None, **kwargs):
        """Loads reports changes into current instance

        >>> self.load_reports_changes()
        [[0 1 2] 4:duplicate_body_content:basic,
        [0 1 2] 4:duplicate_body_content:added]
        >>> self.reports_changes
        [[0 1 2] 4:duplicate_body_content:basic,
        [0 1 2] 4:duplicate_body_content:added]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of report changes
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.reports = connection.get_reports_changes(
            self.account_id, self.project_id, self.id,
            filters=filters, **kwargs
        )
        return self.reports

    def load_downloads(self, connection=None, filters=None, **kwargs):
        """Loads reports downloads into current instance

        >>> self.load_downloads()
        [<deepcrawl.downloads.download.DeepCrawlCrawlDownloads at 0x108a20600>,
        <deepcrawl.downloads.download.DeepCrawlCrawlDownloads at 0x206a226560>
        >>> self.downloads
        [<deepcrawl.downloads.download.DeepCrawlCrawlDownloads at 0x108a20600>,
        <deepcrawl.downloads.download.DeepCrawlCrawlDownloads at 0x206a226560>

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of reports
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.downloads = connection.get_crawl_downloads(
            self.account_id, self.project_id, self.id,
            filters=filters, **kwargs
        )
        return self.downloads

    """
    CRAWL
    """

    def refresh(self, connection=None):
        """Refresh crawl instance

        >>> self.refresh()
        [0 1 3] 2020-04-23 11:10:11+00:00

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: Refreshed crawl
        :rtype: DeepCrawlCrawl
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        crawl = connection.get_crawl(self.account_id, self.project_id, self.id)
        for key in crawl_mutable_fields:
            setattr(self, key, getattr(crawl, key))
        return self

    def update(self, crawl_data, connection=None):
        """Update crawl instance

        >>> self.update(crawl_data)
        [0 1 3] 2020-04-23 11:10:11+00:00

        :param crawl_data: crawl configuration
        :type crawl_data: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: Updated crawl
        :rtype: DeepCrawlCrawl
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        crawl = connection.update_crawl(self.account_id, self.project_id, self.id, crawl_data)
        for key in crawl_mutable_fields:
            setattr(self, key, getattr(crawl, key))
        return self

    def delete(self, connection=None):
        """Delete current crawl instance

        >>> response = self.delete()
        >>> response.status_code
        204

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: HTTP 204 No Content
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        response = connection.delete_crawl(self.account_id, self.project_id, self.id)
        del self
        return response

    """
    REPORTS
    """

    def get_report(self, report_id, connection=None):
        """Get report

        >>> self.get_report("4:duplicate_body_content:basic")
        [0 1 2] 4:duplicate_body_content:basic

        :param report_id: report id
        :type report_id: str
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: report instance
        :rtype: DeepCrawlReport
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_report(self.account_id, self.project_id, self.id, report_id)

    def get_reports(self, use_cache=True, connection=None, filters=None, **kwargs):
        """Get reports for current instance

        * use_cache=True > get_reports will return cached reports or will do a call to DeepCrawl if reports attribute is empty.
        * use_cache=False > get_reports will call DeepCrawl api and will override reports attribute.

        >>> self.get_reports()
        [[0 1 2] 4:duplicate_body_content:basic,
        [0 1 2] 4:duplicate_body_content:added]

        :param use_cache:
        :type use_cache: bool
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: List of reports
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if self.reports and use_cache:
            return self.reports
        return self.load_reports(connection=connection, filters=filters, **kwargs)

    def get_reports_changes(self, use_cache=True, connection=None, filters=None, **kwargs):
        """Get reports changes for current instance

        * use_cache=True > get_reports_changes will return cached reports changes or will do a call to DeepCrawl if reports_changes attribute is empty.
        * use_cache=False > get_reports_changes will call DeepCrawl api and will override reports_changes attribute.

        >>> self.get_reports()
        [[0 1 2] 4:duplicate_body_content:basic,
        [0 1 2] 4:duplicate_body_content:added]

        :param use_cache:
        :type use_cache: bool
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of issues
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if self.reports_changes and use_cache:
            return self.reports_changes
        return self.load_reports_changes(connection=connection, filters=filters, **kwargs)

    """
    DOWNLOADS
    """

    def get_downloads(self, use_cache=True, connection=None, filters=None, **kwargs):
        """Get reports downloads for current instance

        * use_cache=True > get_downloads will return cached reports downloads or will do a call to DeepCrawl if downloads attribute is empty.
        * use_cache=False > get_downloads will call DeepCrawl api and will override downloads attribute.

        >>> self.get_downloads()
        [<deepcrawl.downloads.download.DeepCrawlCrawlDownloads at 0x108a20600>,
        <deepcrawl.downloads.download.DeepCrawlCrawlDownloads at 0x206a226560>

        :param use_cache:
        :type use_cache: bool
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of issues
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if self.downloads and use_cache:
            return self.downloads
        return self.load_downloads(connection=connection, filters=filters, **kwargs)
