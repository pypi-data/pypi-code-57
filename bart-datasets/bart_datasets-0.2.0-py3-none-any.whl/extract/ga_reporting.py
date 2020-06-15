import random
import pandas as pd

from typing import Dict, Any
from datetime import datetime
from apiclient.discovery import build
from google.oauth2.service_account import Credentials


class GoogleAnalyticsReporting:

    SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
    METRICS = [{"expression": "ga:pageviews"}]
    DIMENSIONS = [
        {"name": "ga:dimension1"},
        {"name": "ga:dimension2"},
        {"name": "ga:date"},
    ]
    GA_DATE_FORMAT = "%Y%m%d"
    ENUM_DIMENSIONS = {
        "ga:dimension1": "product_id",
        "ga:dimension2": "customer_id",
        "ga:date": "timestamp",
    }

    def __init__(
        self,
        view_id: str,
        credentials_json_dict: Dict[str, str],
        page_size: int = 10000,
    ) -> None:

        self.view_id = view_id
        self.credentials_json_dict = credentials_json_dict
        self.size = page_size

    def _build_timestamp(self, str_date: str) -> datetime.timestamp:
        return (
            datetime.strptime(str_date, self.GA_DATE_FORMAT)
            .replace(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59),
            )
            .timestamp()
        )

    def _initialize(self) -> Credentials:
        """Initializes an Analytics Reporting API V4 service object.
            Returns:
            An authorized Analytics Reporting API V4 service object.
        """
        credentials = Credentials.from_service_account_info(self.credentials_json_dict)

        # Build the service object.
        analytics = build(
            "analyticsreporting", "v4", credentials=credentials, cache_discovery=False
        )
        return analytics

    def _get_data_report(self, d_ago: int, start: int = 1) -> Dict[str, Any]:
        """Queries the Analytics Reporting API V4.
            Args:
                d_ago: number of days spent to start
                start: start date to process (default:1 or yesterday)
            Returns:
                The Analytics Reporting API V4 response.
        """
        return (
            self._initialize()
            .reports()
            .batchGet(
                body={
                    "reportRequests": [
                        {
                            "viewId": self.view_id,
                            "dateRanges": [
                                {
                                    "startDate": f"{d_ago}daysAgo",
                                    "endDate": f"{start}daysAgo",
                                }
                            ],
                            "metrics": self.METRICS,
                            "dimensions": self.DIMENSIONS,
                            "pageSize": self.size,
                        }
                    ]
                }
            )
            .execute()
        )

    def _data_report2dataframe(self, data_report: Dict[str, Any]) -> pd.DataFrame:
        data = []
        for report in data_report.get("reports", []):
            rows = report.get("data", {}).get("rows", [])
            for row in rows:
                values = {}

                # Get dimensions
                for i, dimension in enumerate(self.DIMENSIONS):
                    key = self.ENUM_DIMENSIONS[dimension["name"]]
                    values[key] = row.get("dimensions", [])[i]

                # Get metric values
                values["action_id"] = 1
                for metric_values in row.get("metrics", []):
                    l_values = metric_values["values"]
                    str_date = values["timestamp"]
                    for _ in range(int(l_values[0])):
                        values["timestamp"] = self._build_timestamp(str_date)
                        data.append(values)

        return pd.DataFrame(
            data, columns=["product_id", "customer_id", "timestamp", "action_id"]
        )

    def extract_data(self, d_ago: int, start: int = 1) -> pd.DataFrame:
        data_report = self._get_data_report(d_ago, start)
        return self._data_report2dataframe(data_report)
