"""
Project
=======
"""

import deepcrawl
from deepcrawl.utils import ImmutableAttributesMixin
from deepcrawl.utils import safe_string_to_datetime
from .extractions import DeepCrawlExtraction
from .project_settings import ProjectSettings

project_extra_fields = (
    "id",
    "account_id",
    "project_settings",
    "majestic_settings",
    "crawls",
    "issues",
    "schedules",
)

project_mutable_fields = project_extra_fields + (
    "crawls_count",
    "issues_count",
    "next_run_time",
    "crawls_finished_last_finished_at",
    "crawls_finished_last_progress_crawled",
    "custom_extractions"
)

project_immutable_fields = (

)

project_fields = project_mutable_fields + project_immutable_fields + project_extra_fields


class DeepCrawlProject(ImmutableAttributesMixin):
    """
    Project Class
    """
    __slots__ = project_fields

    mutable_attributes = project_mutable_fields

    def __init__(self, project_data, account_id):
        # relations
        self.id = project_data.get('id')
        self.account_id = account_id
        self.crawls = []
        self.issues = []
        self.schedules = []

        # attributes
        self.crawls_count = project_data.get('crawls_count')
        self.issues_count = project_data.get('issues_count')
        self.next_run_time = safe_string_to_datetime(project_data.get('next_run_time'))

        self.crawls_finished_last_finished_at = safe_string_to_datetime(
            project_data.get('crawls_finished_last_finished_at')
        )
        self.crawls_finished_last_progress_crawled = project_data.get('crawls_finished_last_progress_crawled')

        # project settings
        self.project_settings = ProjectSettings(project_data)
        self.majestic_settings = None

        # Create a list of custom extractions objects
        self.custom_extractions = [
            DeepCrawlExtraction(extraction_data=extraction) for extraction in project_data['custom_extractions']
        ]

        super(DeepCrawlProject, self).__init__()

    def __repr__(self):
        return f"[{self.account_id} {self.id}] {self.project_settings.name}"

    def __str__(self):
        return f"[{self.account_id} {self.id}] {self.project_settings.name}"

    @property
    def to_dict(self):
        """
        :return: dictionary with the project fields
        :rtype: dict
        """
        dict_ = super(DeepCrawlProject, self).to_dict

        # Remove extra fields
        for attr in project_extra_fields:
            if attr in ["id", "account_id"]:
                continue
            dict_.pop(attr)

        dict_.update(**self.project_settings.to_dict)
        dict_['custom_extractions'] = [x.to_dict for x in self.custom_extractions]

        return dict_

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in project_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in project_immutable_fields}

    def load_crawls(self, connection=None, filters=None, **kwargs):
        """Loads crawls into current instance

        >>> self.load_crawls()
        [[0 1 3] 2020-03-22 12:09:11+00:00,
        [0 1 3] 2020-03-22 11:22:47+00:00]
        >>> self.crawls
        [[0 1 3] 2020-03-22 12:09:11+00:00,
        [0 1 3] 2020-03-22 11:22:47+00:00]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of crawls
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.crawls = connection.get_crawls(self.account_id, self.id, filters=filters, **kwargs)
        return self.crawls

    def load_issues(self, connection=None, filters=None, **kwargs):
        """Loads issues into current instance

        >>> self.load_issues()
        [[0 1 3] Issue Title, [0 1 3] Issue Title2]
        >>> self.issues
        [[0 1 3] Issue Title, [0 1 3] Issue Title2]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of issues
        :rtype: list
        :return:
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.issues = connection.get_issues(self.account_id, self.id, filters=filters, **kwargs)
        return self.issues

    def load_schedules(self, connection=None, filters=None, **kwargs):
        """Loads schedules into current instance

        >>> self.load_schedules()
        [[0 1 3] 2021-06-22 12:09:11+00:00,
        [0 1 3] 2021-04-22 11:22:47+00:00]
        >>> self.schedules
        [[0 1 3] 2021-06-22 12:09:11+00:00,
        [0 1 3] 2021-06-22 11:22:47+00:00]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of schedules
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.schedules = connection.get_schedules(self.account_id, self.id, filters=filters, **kwargs)
        return self.schedules

    """
    PROJECT
    """

    def save(self, connection=None):
        """Save project instance

        * if the instance id is None then the project will be created
        * if the instance id is not None then the project will be updated

        >>> self.save()
        [0 1] www.test.com Project

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: Project instance
        :rtype: DeepCrawlProject
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if not self.id:
            return connection.create_project(self.account_id, self.project_settings.to_dict)
        else:
            return connection.update_project_settings(self.account_id, self.id, self.project_settings.to_dict)

    def refresh(self, connection=None):
        """Makes a call to DeepCrawl in order to refresh the current instance.

        >>> self.refresh()
        [0 1] www.test.com Project

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: refreshed instance
        :rtype: DeepCrawlProject
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        project = connection.get_project(self.account_id, self.id)
        for key in self.__slots__:
            setattr(self, key, getattr(project, key))
        return self

    def update_settings(self, project_settings, connection=None):
        """Updates current project instance with another project_settings.
        Settings argument can be dict or a ProjectSettings instance.

        >>> self.update_settings(project_settings)
        [0 1] www.test.com Project Updated

        :param project_settings: new settings configuration
        :type project_settings: dict or ProjectSettings
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection

        :returns: the updated project instance
        :rtype: DeepCrawlProject
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        project = connection.update_project_settings(self.account_id, self.id, project_settings)
        self.project_settings = project.project_settings
        return self

    def delete(self, connection=None):
        """Delete current project instance

        >>> response = self.delete()
        >>> response.status_code
        204

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: HTTP 204 No Content
        """
        response = connection.delete_project(self.account_id, self.id)
        return response

    def add_extractions(self, extractions, connection=None):
        """Add extractions to current project

        .. code-block::

            extractions = [
                {
                  "label": str,
                  "regex": "regex",
                  "clean_html_tags": bool,
                  "match_number_from": int,
                  "match_number_to": int,
                  "filter": "regex"
                }
            ]

        >>> self.add_extractions(extractions)

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :param extractions: list of dictionaries or list of DeepCrawlExtraction instances or combined
        :type extractions: list
        :return: project with updated extractions
        :rtype: DeepCrawlProject
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        extractions_list = ([x.to_dict for x in self.custom_extractions])

        for extraction in extractions:
            if isinstance(extraction, DeepCrawlExtraction):
                extractions_list.append(extraction.to_dict)
                self.custom_extractions.append(extraction)
            else:
                extractions_list.append(extraction)
                self.custom_extractions.append(DeepCrawlExtraction(extraction_data=extraction))

        new_settings = {'custom_extractions': extractions_list}
        return connection.update_project_settings(self.account_id, self.id, new_settings)

    """
    MAJESTIC
    """

    def get_majestic_settings(self, connection=None):
        """Update majestic settings

        >>> self.get_majestic_settings()
        [<deepcrawl.projects.majestic_settings.MajesticSettings at 0x108a20600>,
        <deepcrawl.projects.majestic_settings.MajesticSettings at 0x108a20600>]

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: majestic settings instance
        :rtype: MajesticSettings
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.majestic_settings = connection.get_majestic_settings(self.account_id, self.id)
        return self.majestic_settings

    def refresh_majestic_settings(self, connection=None):
        """Refresh majestic settings

        >>> self.refresh_majestic_settings()
        [<deepcrawl.projects.majestic_settings.MajesticSettings at 0x108a20600>,
        <deepcrawl.projects.majestic_settings.MajesticSettings at 0x108a20600>]

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: refreshed majestic settings
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.majestic_settings = self.get_majestic_settings(connection=connection)
        return self.majestic_settings

    def update_majestic_settings(self, majestic_settings, connection=None):
        """Update majestic settings.
        Majestic settings argument can be dict or a MajesticSettings instance.

        >>> self.update_majestic_settings(majestic_settings)
        [<deepcrawl.projects.majestic_settings.MajesticSettings at 0x108a20600>,
        <deepcrawl.projects.majestic_settings.MajesticSettings at 0x108a20600>]

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :param majestic_settings: majestic settings
        :type majestic_settings: dict or MajesticSettings
        :return: updated majestic settings
        :rtype: MajesticSettings
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.majestic_settings = connection.update_majestic_settings(self.account_id, self.id, majestic_settings)
        return self.majestic_settings

    """
    ISSUES
    """

    def create_issue(self, issue_data, connection=None):
        """Create issue

        >>> self.create_issue(issue_data)
        [0 1 4] Issue Title

        :param issue_data: issue configuration
        :type issue_data: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: issue instance
        :rtype: DeepCrawlIssue
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        issue = connection.create_issue(self.account_id, self.id, issue_data)
        return issue

    def get_issue(self, issue_id, connection=None):
        """Get issue

        >>> self.get_issue(3)
        [0 1 3] Issue Title

        :param issue_id: issue id
        :type issue_id: int
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: issue instance
        :rtype: DeepCrawlIssue
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        issue = connection.get_issue(self.account_id, self.id, issue_id)
        return issue

    def update_issue(self, issue_id, issue_data, connection=None):
        """Update issue

        >>> self.update_issue(3, issue_data)
        [0 1 3] Issue Title updated

        :param issue_id: issue id
        :type issue_id: int
        :param issue_data: issue configuration
        :type issue_data: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return:
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        issue = connection.update_issue(self.account_id, self.id, issue_id, issue_data)
        return issue

    def delete_issue(self, issue_id, connection=None):
        """Delete current issue instance

        >>> response = self.delete_issue(3)
        >>> response.status_code
        204

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: HTTP 204 No Content
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        response = connection.delete_issue(self.account_id, self.id, issue_id)
        return response

    def get_issues(self, use_cache=True, connection=None, filters=None, **kwargs):
        """Get issues for current instance

        * use_cache=True > get_issues will return cached issues or will do a call to DeepCrawl if issues attribute is empty.
        * use_cache=False > get_issues will call DeepCrawl api and will override issues attribute.

        >>> self.get_issues()
        [[0 1 3] Issue Title, [0 1 4] Issue Title updated]

        :param use_cache:
        :type use_cache: bool
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: list of issues
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if use_cache and self.issues:
            return self.issues
        return self.load_issues(connection=connection, filters=filters, **kwargs)

    """
    CRAWLS
    """

    def start_crawl(self, connection=None):
        """Start a new crawl

        >>> response = self.start_crawl()
        >>> response.status_code
        201

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: HTTP 201 Created
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.start_crawl(self.account_id, self.id)

    def create_crawl(self, crawl_data, connection=None):
        """Create crawl

        >>> self.create_crawl(crawl_data)
        [0 1 3] 2020-03-22 12:09:11+00:00

        :param crawl_data: crawl configuration
        :type crawl_data: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: crawl instance
        :rtype: DeepCrawlCrawl
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.create_crawl(self.account_id, self.id, crawl_data)

    def get_crawl(self, crawl_id, connection=None):
        """Get crawl

        >>> self.get_crawl(3)
        [0 1 3] 2020-03-22 12:09:11+00:00

        :param crawl_id: crawl id
        :type crawl_id: int
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: crawl instance
        :rtype: DeepCrawlCrawl
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_crawl(self.account_id, self.id, crawl_id)

    def update_crawl(self, crawl_id, crawl_data, connection=None):
        """Update crawl

        >>> self.update_crawl(3, crawl_data)
        [0 1 3] 2020-04-23 11:10:11+00:00

        :param crawl_id: crawl id
        :type crawl_id: int
        :param crawl_data: crawl configuration
        :type crawl_data: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: updated crawl instance
        :rtype: DeepCrawlCrawl
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        crawl = connection.update_crawl(self.account_id, self.id, crawl_id, crawl_data)
        return crawl

    def delete_crawl(self, crawl_id, connection=None):
        """Delete current crawl instance

        >>> response = self.delete_crawl(3)
        >>> response.status_code
        204

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: HTTP 204 No Content
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.delete_crawl(self.account_id, self.id, crawl_id)

    def get_crawls(self, use_cache=True, connection=None, filters=None, **kwargs):
        """Get issues for current instance

        * use_cache=True > get_crawls will return cached crawls or will do a call to DeepCrawl if crawls attribute is empty.
        * use_cache=False > get_crawls will call DeepCrawl api and will override crawls attribute.

        >>> self.get_crawls()
        [[0 1 3] 2020-04-23 11:10:11+00:00, [0 1 4] 2020-04-23 11:10:11+00:00]

        :param use_cache:
        :type use_cache: bool
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: list of crawls
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if use_cache and self.crawls:
            return self.crawls
        return self.load_crawls(connection=connection, filters=filters, **kwargs)

    """
    SCHEDULES
    """

    def create_schedule(self, schedule_data, connection=None):
        """Create schedule

        >>> self.create_schedule(schedule_data)
        [0 1 4] 2021-03-22 12:09:11+00:00

        :param schedule_data: schedule configuration
        :type schedule_data: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: schedule instance
        :rtype: DeepCrawlSchedule
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.create_schedule(self.account_id, self.id, schedule_data)

    def get_schedule(self, schedule_id, connection=None):
        """Get schedule

        >>> self.get_schedule(3)
        [0 1 3] 2021-03-22 12:09:11+00:00

        :param schedule_id: issue id
        :type schedule_id: int
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: schedule instance
        :rtype: DeepCrawlSchedule
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_schedule(self.account_id, self.id, schedule_id)

    def update_schedule(self, schedule_id, schedule_data, connection=None):
        """Update schedule

        >>> self.update_schedule(3, schedule_data)
        [0 1 3] 2021-04-22 12:09:11+00:00

        :param schedule_id: issue id
        :type schedule_id: int
        :param schedule_data: schedule configuration
        :type schedule_data: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: updated schedule instance
        :rtype: DeepCrawlSchedule
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        schedule = connection.update_schedule(self.account_id, self.id, schedule_id, schedule_data)
        return schedule

    def delete_schedule(self, schedule_id, connection=None):
        """Delete current schedule instance

        >>> response = self.delete_schedule(3)
        >>> response.status_code
        204

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: HTTP 204 No Content
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.delete_schedule(self.account_id, self.id, schedule_id)

    def get_schedules(self, use_cache=True, connection=None, filters=None, **kwargs):
        """Get schedules for current instance

        * use_cache=True > get_schedules will return cached schedules or will do a call to DeepCrawl if schedules attribute is empty.
        * use_cache=False > get_schedules will call DeepCrawl api and will override schedules attribute.

        >>> self.get_schedules()
        [[0 1 3] 2021-03-22 12:09:11+00:00, [0 1 4] 2021-03-22 12:09:11+00:00]

        :param use_cache:
        :type use_cache: bool
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :param filters: filters dict
        :type filters: dict
        :param kwargs: extra arguments like pagination arguments
        :type kwargs: dict
        :return: list of schedules
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if use_cache and self.schedules:
            return self.schedules
        return self.load_schedules(connection=connection, filters=filters, **kwargs)
