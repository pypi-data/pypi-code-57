"""
Account
=======
"""

import deepcrawl
from deepcrawl.utils import ImmutableAttributesMixin, safe_string_to_datetime


account_extra_fields = (
    "id",
    "projects",
)

account_mutable_fields = account_extra_fields + (
    'active',
    'address_city',
    'address_state',
    'address_street',
    'address_zip',
    'api_callback',
    'api_callback_headers',
    'country',
    'custom_color_header',
    'custom_color_menu',
    'custom_domain',
    'custom_email_footer',
    'custom_logo_file',
    'custom_support_email',
    'custom_support_phone',
    'custom_skin_name',
    'finance_vat',
    'has_annual_package',
    'static_location',
    'custom_proxy',
    'custom_proxy_read_only',
    'name',
    'phone',
    'pref_email_support',
    'credits_available',
    'projects_count',
    'active_projects_count',
    'active_projects_refresh_at',
    'credit_allocation_refresh_at',
    'limit_projects_max',
    'limit_levels_max',
    'limit_pages_max',
    'timezone',
    'chargebee',
    'chargebee_subscription',
    'is_annual',
    'additional_users_available',
    'number_of_users',
    'limit_users_max',
    'portal_disabled',
    'currency',
    'account_managers',
    'splunk_enabled',
    'crawl_rate_max',
)

account_immutable_fields = (
    '_primary_account_package_href',
    '_subscription_href',
    '_href',
    '_projects_href',
    '_hosted_page_href',
    '_crawls_href',
    '_credit_allocations_href',
    '_credit_reports_href',
    '_locations_href',
)

account_fields = account_mutable_fields + account_immutable_fields


class DeepCrawlAccount(ImmutableAttributesMixin):
    """
    Account class
    """
    __slots__ = account_fields

    mutable_attributes = account_mutable_fields
    post_fields = ['address_city', 'address_street', 'country', 'custom_color_header', 'limit_levels_max',
                   'limit_pages_max', 'custom_color_menu', 'name', 'phone', 'address_zip', 'pref_email_support',
                   'custom_domain', 'address_state', 'custom_support_email', 'custom_support_phone', 'timezone',
                   'finance_vat', 'splunk_enabled', 'active']

    def __init__(self, account_data):
        self.id = account_data.get("id")
        self.projects = []

        self.active = account_data.get('active')
        self.address_city = account_data.get('address_city')
        self.address_state = account_data.get('address_state')
        self.address_street = account_data.get('address_street')
        self.address_zip = account_data.get('address_zip')
        self.api_callback = account_data.get('api_callback')
        self.api_callback_headers = account_data.get('api_callback_headers')
        self.country = account_data.get('country')
        self.custom_color_header = account_data.get('custom_color_header')
        self.custom_color_menu = account_data.get('custom_color_menu')
        self.custom_domain = account_data.get('custom_domain')
        self.custom_email_footer = account_data.get('custom_email_footer')
        self.custom_logo_file = account_data.get('custom_logo_file')
        self.custom_support_email = account_data.get('custom_support_email')
        self.custom_support_phone = account_data.get('custom_support_phone')
        self.custom_skin_name = account_data.get('custom_skin_name')
        self.finance_vat = account_data.get('finance_vat')
        self.has_annual_package = account_data.get('has_annual_package')
        self.static_location = account_data.get('static_location')
        self.custom_proxy = account_data.get('custom_proxy')
        self.custom_proxy_read_only = account_data.get('custom_proxy_read_only')
        self.name = account_data.get('name')
        self.phone = account_data.get('phone')
        self.pref_email_support = account_data.get('pref_email_support')
        self.credits_available = account_data.get('credits_available')
        self.projects_count = account_data.get('projects_count')
        self.active_projects_count = account_data.get('active_projects_count')
        self.active_projects_refresh_at = account_data.get('active_projects_refresh_at')
        self.credit_allocation_refresh_at = safe_string_to_datetime(
            account_data.get('credit_allocation_refresh_at')
        )
        self.limit_projects_max = account_data.get('limit_projects_max')
        self.limit_levels_max = account_data.get('limit_levels_max')
        self.limit_pages_max = account_data.get('limit_pages_max')
        self.timezone = account_data.get('timezone')
        self.chargebee = account_data.get('chargebee')
        self.chargebee_subscription = account_data.get('chargebee_subscription')
        self.is_annual = account_data.get('is_annual')
        self.additional_users_available = account_data.get('additional_users_available')
        self.number_of_users = account_data.get('number_of_users')
        self.limit_users_max = account_data.get('limit_users_max')
        self.portal_disabled = account_data.get('portal_disabled')
        self.currency = account_data.get('currency')
        self.account_managers = account_data.get('account_managers')
        self.splunk_enabled = account_data.get('splunk_enabled')
        self.crawl_rate_max = account_data.get('crawl_rate_max')
        self._primary_account_package_href = account_data.get('_primary_account_package_href')
        self._subscription_href = account_data.get('_subscription_href')
        self._href = account_data.get('_href')
        self._projects_href = account_data.get('_projects_href')
        self._hosted_page_href = account_data.get('_hosted_page_href')
        self._crawls_href = account_data.get('_crawls_href')
        self._credit_allocations_href = account_data.get('_credit_allocations_href')
        self._credit_reports_href = account_data.get('_credit_reports_href')
        self._locations_href = account_data.get('_locations_href')

        super(DeepCrawlAccount, self).__init__()

    def __repr__(self):
        return f"[{self.id}] {self.name}"

    def __str__(self):
        return f"[{self.id}] {self.name}"

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in account_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in account_immutable_fields}

    def load_projects(self, connection=None, filters=None, **kwargs):
        """Loads projects into current instance

        >>> self.load_projects()
        [[0 1] www.test.com Project, [0 2] www.test2.com Project]
        >>> self.projects
        [[0 1] www.test.com Project, [0 2] www.test2.com Project]

        :param filters: filters dict
        :type filters: dict
        :param kwargs: pagination arguments
        :type kwargs: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: list of projects
        :rtype: list
        :return:
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        self.projects = connection.get_projects(self.id, filters=filters, **kwargs)
        return self.projects

    """
    ACCOUNT
    """

    def save(self, connection=None):
        """Save account instance

        * if the instance id is None then the account will be created
        * if the instance id is not None then the account will be updated

        >>> self.save()
        [0] DeepCrawlAccount

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: Account instance
        :rtype: DeepCrawlAccount
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if not self.id:
            return connection.create_account({key: getattr(self, key) for key in self.post_fields})
        else:
            return connection.update_account(self.id, {key: getattr(self, key) for key in self.post_fields})

    def refresh(self, connection=None):
        """Makes a call to DeepCrawl in order to refresh the current instance.

        >>> self.refresh()
        [0] DeepCrawlAccount

        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: refreshed instance
        :rtype: DeepCrawlAccount
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        account = connection.get_account(self.id)
        for key in account_mutable_fields:
            setattr(self, key, getattr(account, key))
        return self

    def update(self, account_settings, connection=None):
        """Updates an instance with account_settings

        >>> self.update(account_settings)
        [0] DeepCrawlAccount

        :param account_settings: dictionary with the new configuration
        :type account_settings: dict
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection

        :returns: the updated account instance
        :rtype: DeepCrawlAccount
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        account = connection.update_account(self.id, account_settings)
        for key in account_mutable_fields:
            setattr(self, key, getattr(account, key))
        return self

    """
    PROJECTS
    """
    def create_project(self, project_settings, connection=None):
        """Create project.
        Project settings argument can be dict or a ProjectSettings instance.

        >>> self.create_project(project_settings)
        [0 1] www.test.com Project

        :param project_settings: project configuration
        :type project_settings: dict or ProjectSettings
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: Project instance
        :rtype: DeepCrawlProject
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.create_project(self.id, project_settings)

    def get_project(self, project_id, connection=None):
        """Get Project

        >>> self.get_project(1)
        [0 1] www.test.com Project

        :param project_id: project id
        :type project_id: int
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: Requested project
        :rtype: DeepCrawlProject
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.get_project(self.id, project_id)

    def update_project_settings(self, project_id, settings, connection=None):
        """Update the project settings.
        Settings argument can be dict or a ProjectSettings instance.

        >>> self.update_project_settings(1, settings)
        [0 1] www.test.com Project

        :param project_id: project id
        :type project_id: int
        :param settings: new settings configuration
        :type settings: dict or ProjectSettings
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: Updated project
        :rtype: DeepCrawlProject
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.update_project_settings(self.id, project_id, settings)

    def delete_project(self, project_id, connection=None):
        """Delete project

        >>> response = self.delete_project(1)
        >>> response.status_code
        204

        :param project_id: project id
        :type project_id: int
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :return: HTTP 204 No Content
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        return connection.delete_project(self.id, project_id)

    def get_projects(self, use_cache=True, connection=None, filters=None):
        """Get projects

        * use_cache=True > get_projects will return cached projects or will do a call to DeepCrawl if projects attribute is empty.
        * use_cache=False > get_projects will call DeepCrawl api and will override projects attribute.

        >>> self.get_projects()
        [[0 1] www.test.com Project, [0 2] www.test2.com Project]

        :param use_cache:
        :type use_cache: bool
        :param connection: connection
        :type connection: deepcrawl.DeepCrawlConnection
        :param filters: filters dict
        :return: list of projects
        :rtype: list
        """
        connection = connection or deepcrawl.DeepCrawlConnection.get_instance()
        if use_cache and self.projects:
            return self.projects
        return self.load_projects(connection=connection, filters=filters)
