"""
Crawls Connection
=================
"""

from deepcrawl.api import ApiConnection
from deepcrawl.api.api_endpoints import get_api_endpoint
from .crawl import DeepCrawlCrawl
from .schedule import DeepCrawlSchedule


class CrawlConnection(ApiConnection):
    """
    CRAWL

        * endpoint: /accounts/{account_id}/projects/{project_id}/crawls
        * http methods: GET, POST
        * methods: get_crawls, start_crawl

        - endpoint: /accounts/{account_id}/projects/{project_id}/crawls/{crawl_id}
        - http methods: GET, PATCH, DELETE
        - methods: get_crawl, update_crawl, delete_crawl

    SCHEDULES
        * endpoint: /accounts/{account_id}/projects/{project_id}/schedules
        * http methods: GET, POST
        * methods: create_schedule, get_schedules

        - endpoint: /accounts/{account_id}/projects/{project_id}/schedules/{schedule_id}
        - http methods: GET, PATCH, DELETE
        - methods: get_schedule, update_schedule, delete_schedule
    """

    """
    CRAWL
    """

    def start_crawl(self, account_id, project_id):
        """Start Crawl

        >>> response = connection.start_crawl(0, 1)
        >>> response.status_code
        201

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :return: HTTP 201 Created
        """
        endpoint_url = get_api_endpoint(endpoint='crawls', account_id=account_id, project_id=project_id)
        crawl_start_data = {"status": "crawling"}
        return self.dc_request(url=endpoint_url, method='post', content_type='form', data=crawl_start_data)

    def create_crawl(self, account_id, project_id, crawl_data):
        """Create crawl

        .. code-block::

            crawl_data = {
                "status": str,
                "limit_levels_max": int,
                "limit_pages_max": int,
                "auto_finalize": str
            }

        >>> connection.create_crawl(0, 1, crawl_data)
        [0 1 3] 2020-04-23 11:10:11+00:00

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param crawl_data: crawl configuration
        :type crawl_data: dict
        :return: Crawl instance
        :rtype: DeepCrawlCrawl
        """
        endpoint_url = get_api_endpoint(endpoint='crawls', account_id=account_id, project_id=project_id)
        response = self.dc_request(url=endpoint_url, method='post', json=crawl_data)
        return DeepCrawlCrawl(crawl_data=response.json(), account_id=account_id, project_id=project_id)

    def get_crawl(self, account_id, project_id, crawl_id):
        """Get crawl

        >>> connection.get_crawl(0, 1, 3)
        [0 1 3] 2020-04-23 11:10:11+00:00

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param crawl_id: project id
        :type crawl_id: int
        :return: Requested crawl
        :rtype: DeepCrawlCrawl
        """
        endpoint_url = get_api_endpoint(
            endpoint='crawl',
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        response = self.dc_request(url=endpoint_url, method='get')
        return DeepCrawlCrawl(crawl_data=response.json(), account_id=account_id, project_id=project_id)

    def update_crawl(self, account_id, project_id, crawl_id, crawl_data):
        """Update crawl

        >>> connection.update_crawl(0, 1, 3, crawl_data)
        [0 1 3] 2020-04-23 11:10:11+00:00

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param crawl_id: crawl id
        :type crawl_id: int
        :param crawl_data: crawl configuration
        :type crawl_data: dict
        :return: Updated crawl
        :rtype: DeepCrawlCrawl
        """
        endpoint_url = get_api_endpoint(
            endpoint='crawl',
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        response = self.dc_request(url=endpoint_url, method='patch', json=crawl_data)
        return DeepCrawlCrawl(crawl_data=response.json(), account_id=account_id, project_id=project_id)

    def delete_crawl(self, account_id, project_id, crawl_id):
        """Delete crawl

        >>> response = connection.delete_crawl(0, 1, 3)
        >>> response.status_code
        204

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param crawl_id: crawl id
        :type crawl_id: int
        :return: HTTP 204 No Content
        """
        endpoint_url = get_api_endpoint(
            endpoint='crawl',
            account_id=account_id, project_id=project_id, crawl_id=crawl_id
        )
        return self.dc_request(url=endpoint_url, method='delete')

    def get_crawls(self, account_id, project_id, filters=None, **kwargs):
        """Get crawls

        >>> connection.get_crawls(0, 1)
        [[0 1 3] 2020-04-23 11:10:11+00:00, [0 1 4] 2020-04-23 11:10:11+00:00]

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param filters: filters
        :type filters: dict
        :param kwargs: extra arguments, like pagination ones
        :type kwargs: dict
        :return: list of crawls
        :rtype: list
        """
        endpoint_url = get_api_endpoint(endpoint='crawls', account_id=account_id, project_id=project_id)
        crawls = self.get_paginated_data(url=endpoint_url, method='get', filters=filters, **kwargs)

        list_of_crawls = []
        for project in crawls:
            list_of_crawls.append(
                DeepCrawlCrawl(crawl_data=project, account_id=account_id, project_id=project_id)
            )
        return list_of_crawls

    """
    SCHEDULES
    """

    def create_schedule(self, account_id, project_id, schedule_data):
        """Create schedule

        >>> connection.create_schedule(0, 1, schedule_data)
        [0 1 4] 2021-03-22 12:09:11+00:00

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param schedule_data: schedule configuration
        :type schedule_data: dict
        :return: schedule instance
        :rtype: DeepCrawlSchedule
        """
        endpoint_url = get_api_endpoint(endpoint='crawl_schedules', account_id=account_id, project_id=project_id)
        response = self.dc_request(url=endpoint_url, method='post', json=schedule_data)
        return DeepCrawlSchedule(account_id=account_id, project_id=project_id, schedule_data=response.json())

    def get_schedule(self, account_id, project_id, schedule_id):
        """Get schedule

        >>> connection.get_schedule(1, 2, 3)
        [0 1 3] 2021-03-22 12:09:11+00:00

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param schedule_id: issue id
        :type schedule_id: int
        :return: schedule instance
        :rtype: DeepCrawlSchedule
        """
        endpoint_url = get_api_endpoint(
            endpoint='crawl_schedule',
            account_id=account_id, project_id=project_id, schedule_id=schedule_id
        )
        response = self.dc_request(url=endpoint_url, method='get')
        return DeepCrawlSchedule(account_id=account_id, project_id=project_id, schedule_data=response.json())

    def update_schedule(self, account_id, project_id, schedule_id, schedule_data):
        """Update schedule

        >>> connection.update_schedule(1, 2, 3, schedule_data)
        [0 1 3] 2021-04-22 12:09:11+00:00

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param schedule_id: issue id
        :type schedule_id: int
        :param schedule_data: schedule configuration
        :type schedule_data: dict
        :return: updated schedule instance
        :rtype: DeepCrawlSchedule
        """
        endpoint_url = get_api_endpoint(
            endpoint='crawl_schedule',
            account_id=account_id, project_id=project_id, schedule_id=schedule_id
        )
        response = self.dc_request(url=endpoint_url, method='patch', json=schedule_data)
        return DeepCrawlSchedule(account_id=account_id, project_id=project_id, schedule_data=response.json())

    def delete_schedule(self, account_id, project_id, schedule_id):
        """Delete current schedule instance

        >>> response = connection.delete_schedule(1, 2, 3)
        >>> response.status_code
        204

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param schedule_id: issue id
        :type schedule_id: int
        :return: HTTP 204 No Content
        """
        endpoint_url = get_api_endpoint(
            endpoint='crawl_schedule',
            account_id=account_id, project_id=project_id, schedule_id=schedule_id
        )
        return self.dc_request(url=endpoint_url, method='delete')

    def get_schedules(self, account_id, project_id, filters=None, **kwargs):
        """Get schedules

        >>> connection.get_schedules(1, 2)
        [[0 1 3] 2021-03-22 12:09:11+00:00, [0 1 4] 2021-03-22 12:09:11+00:00]

        :param account_id: account id
        :type account_id: int
        :param project_id: project id
        :type project_id: int
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: list of schedules
        :rtype: list
        """
        endpoint_url = get_api_endpoint(endpoint='crawl_schedules', account_id=account_id, project_id=project_id)
        schedules = self.get_paginated_data(url=endpoint_url, method='get', filters=filters, **kwargs)

        list_of_schedules = []
        for schedule in schedules:
            list_of_schedules.append(
                DeepCrawlSchedule(account_id=account_id, project_id=project_id, schedule_data=schedule)
            )
        return list_of_schedules
