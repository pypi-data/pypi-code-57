from deepcrawl.exceptions import InvalidDcUrl

DC_BASE_URL = "https://api.deepcrawl.com/"

ENDPOINTS = {
    # auth
    "session": "sessions",

    # Accounts
    "account": "accounts/{account_id}",
    "accounts": "accounts",

    # Projects
    "project": "accounts/{account_id}/projects/{project_id}",
    "projects": "accounts/{account_id}/projects",

    "majestic": "accounts/{account_id}/projects/{project_id}/majestic_configuration",

    "issue": "accounts/{account_id}/projects/{project_id}/issues/{issue_id}",
    "issues": "accounts/{account_id}/projects/{project_id}/issues",

    # Crawls
    "crawl": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}",
    "crawls": "accounts/{account_id}/projects/{project_id}/crawls",

    "crawl_schedule": "accounts/{account_id}/projects/{project_id}/schedules/{schedule_id}",
    "crawl_schedules": "accounts/{account_id}/projects/{project_id}/schedules",

    # Reports
    "report": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}",
    "reports": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports",
    "reports_changes": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/changes",

    "report_row": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                  "report_rows/{report_row_id}",
    "report_rows": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                   "report_rows",
    "report_trend": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                    "statistics/report_trend",

    # Downloads
    "crawl_downloads": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/downloads",
    "report_download": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                       "downloads/{report_download_id}",
    "report_downloads": "accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}/reports/{report_id}/"
                        "downloads"
}


def get_api_endpoint(endpoint: str, **kwargs):
    """
    >>> get_api_endpoint("report", account_id=1, project_id=2, crawl_id=3, report_id=4)
    """

    try:
        return f"{DC_BASE_URL}{ENDPOINTS.get(endpoint).format(**kwargs)}"
    except Exception:
        raise InvalidDcUrl("Invalid url name or invalid kwargs send.")
