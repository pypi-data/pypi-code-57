"""
Reports Connection
==================
"""

from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint
from .report import DeepCrawlReport
from .report_row import DeepCrawlReportRow


class ReportConnection(ApiConnection):
    """
    REPORT
        * endpoint: /accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports
        * http methods: GET
        * methods: get_reports

        - endpoint: /accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}
        - http methods: GET
        - methods: get_report

        * endpoint: /accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/changes
        * http methods: GET, HEAD
        * methods: get_reports_changes

    REPORT ROWS
        * endpoint: /accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/report_rows
        * http methods: GET
        * methods: get_report_rows, get_report_row_count

        - endpoint: /accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/report_rows/{report_row_id}
        - http methods: GET
        - methods: get_report_row

    """

    """
    REPORT
    """

    def get_report(self, account_id, project_id, crawl_id, report_id):
        """Get report

        >>> connection.get_report(0, 1, 2, "duplicate_body_content:basic")
        [0 1 2] 4:duplicate_body_content:basic

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param crawl_id: crawl id
        :type crawl_id: int
        :param report_id: report id
        :type report_id: str
        :return: Requested report
        :rtype: DeepCrawlReport
        """
        request_url = get_api_endpoint(
            "report",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, report_id=report_id
        )
        response = self.dc_request(url=request_url, method='get')
        return DeepCrawlReport(
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_data=response.json()
        )

    def get_reports(self, account_id, project_id, crawl_id, filters=None, **kwargs):
        """Get reports

        >>> connection.get_reports(0, 1, 2)
        [[0 1 2] 4:duplicate_body_content:basic,
        [0 1 2] 4:duplicate_body_content:added]

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param crawl_id: crawl id
        :type crawl_id: int
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: List of reports
        :rtype: list
        """
        request_url = get_api_endpoint(
            "reports",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        reports_response = self.get_paginated_data(request_url, method='get', filters=filters, **kwargs)

        list_of_reports = []
        for report in reports_response:
            list_of_reports.append(DeepCrawlReport(
                project_id=project_id, account_id=account_id, crawl_id=crawl_id,
                report_data=report
            ))
        return list_of_reports

    def get_reports_changes(self, account_id, project_id, crawl_id, filters=None, **kwargs):
        """Get reports changes

        >>> connection.get_reports_changes(0, 1, 2)
        [[0 1 2] 4:duplicate_body_content:removed,
        [0 1 2] 4:duplicate_body_content:added]

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param crawl_id: crawl id
        :type crawl_id: int
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: List of reports
        :rtype: list
        """
        request_url = get_api_endpoint(
            "reports_changes",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        reports_changes_response = self.get_paginated_data(request_url, method='get', filters=filters, **kwargs)
        list_of_reports_changes = []
        for report in reports_changes_response:
            list_of_reports_changes.append(DeepCrawlReport(
                project_id=project_id, account_id=account_id, crawl_id=crawl_id,
                report_data=report
            ))
        return list_of_reports_changes

    """
    REPORT ROW
    """

    def get_report_row(self, account_id, project_id, crawl_id, report_id, report_row_id):
        """Get report row

        >>> connection.get_report_row(0, 1, 2, "duplicate_body_content:basic", 6)
        <deepcrawl.reports.report_row.DeepCrawlReportRow at 0x108a20600>

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param crawl_id: crawl id
        :type crawl_id: int
        :param report_id: report id
        :type report_id: str
        :param report_row_id: report row id
        :type report_row_id: str
        :return: Requested report row
        :rtype: DeepCrawlReportRow
        """
        request_url = get_api_endpoint(
            "report_row",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_id=report_id, report_row_id=report_row_id
        )
        response = self.dc_request(url=request_url, method='get')
        return DeepCrawlReportRow(
            account_id=account_id, project_id=project_id, crawl_id=crawl_id, report_id=report_id,
            row_data=response.json()
        )

    def get_report_rows(self, account_id, project_id, crawl_id, report_id, filters=None, **kwargs):
        """Get report rows

        >>> connection.get_report_rows(0, 1, 2, "duplicate_body_content:basic")
        [<deepcrawl.reports.report_row.DeepCrawlReportRow at 0x108a20600>,
        <deepcrawl.reports.report_row.DeepCrawlReportRow at 0x148a25670>]

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param crawl_id: crawl id
        :type crawl_id: int
        :param report_id: report id
        :type report_id: str
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: List of report rows
        :rtype: list
        """
        request_url = get_api_endpoint(
            "report_rows",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_id=report_id
        )
        rows_response = self.get_paginated_data(request_url, method='get', filters=filters, **kwargs)

        list_of_rows = []
        for row in rows_response:
            list_of_rows.append(DeepCrawlReportRow(
                project_id=project_id, account_id=account_id, crawl_id=crawl_id,
                report_id=report_id, row_data=row
            ))
        return list_of_rows

    def get_report_row_count(self, account_id, project_id, crawl_id, report_id, filters=None):
        """Get report row count

        >>> connection.get_report_row_count(0, 1, 2, "duplicate_body_content:basic")
        "2"

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param crawl_id: crawl id
        :type crawl_id: int
        :param report_id: report id
        :type report_id: str
        :param filters: filters dict
        :type filters: dict
        :return: Count of report row
        :rtype: str
        """
        request_url = get_api_endpoint(
            "report_rows",
            account_id=account_id, project_id=project_id, crawl_id=crawl_id,
            report_id=report_id
        )
        response = self.dc_request(url=request_url, method='head', filters=filters)
        return response.headers.get('X-Records')
