"""
Project Settings
================
"""

from deepcrawl.utils import ImmutableAttributesMixin

settings_mutable_fields = (
    'alert_emails',
    'alert_setting',
    'api_callback',
    'api_callback_headers',
    'attach_pdf',
    'auto_finalize',
    'clean_custom_extraction',
    'compare_to',
    'crawl_amphtml_ext',
    'crawl_amphtml_int',
    'crawl_canonicals_ext',
    'crawl_canonicals_int',
    'crawl_hyperlinks_ext',
    'crawl_hyperlinks_int',
    'crawl_hreflangs_ext',
    'crawl_hreflangs_int',
    'crawl_images_ext',
    'crawl_images_int',
    'crawl_media_mobile_ext',
    'crawl_media_mobile_int',
    'crawl_paginations_ext',
    'crawl_paginations_int',
    'crawl_redirects_ext',
    'crawl_redirects_int',
    'crawl_scripts_ext',
    'crawl_scripts_int',
    'crawl_stylesheets_ext',
    'crawl_stylesheets_int',
    'crawl_disallow_1st_level',
    'crawl_not_included_1st_level',
    'crawl_nofollow',
    'crawl_noindex',
    'crawl_non_html',
    'crawl_css_js',
    'crawl_disallowed_pages',
    'crawl_external_urls',
    'crawl_nofollow_links',
    'crawl_noindex_pages',
    'crawl_non_html_file_types',
    'crawl_not_included_urls',
    'crawl_rate',
    'crawl_rate_advanced',
    'crawl_subdomains',
    'crawl_http_and_https',
    'crawl_test_site',
    'crawl_types',
    'custom_dns',
    'custom_header_user_agent',
    'custom_header_user_agent_short',
    'is_stealth_mode',
    'deepcrawl_bot_url',
    'duplicate_precision',
    'low_log_summary_requests',
    'high_log_summary_requests',
    'limit_levels_max',
    'limit_pages_max',
    'location',
    'max_content_size',
    'max_description_length',
    'max_external_links',
    'max_html_size',
    'max_links',
    'max_load_time',
    'max_redirections',
    'max_title_width',
    'max_url_length',
    'min_content_ratio',
    'thin_page_threshold',
    'min_description_length',
    'min_title_length',
    'empty_page_threshold',
    'name',
    'page_groupings',
    'robots_overwrite',
    'site_primary',
    'site_secondaries',
    'site_test',
    'site_test_pass',
    'site_test_user',
    'start_urls',
    'url_rewrite_query_parameters',
    'url_rewrite_regex_parameters',
    'url_rewrite_strip_fragment',
    'urls_excluded',
    'urls_included',
    'use_rewrite_rules',
    'use_robots_overwrite',
    'user_agent',
    'mobile_user_agent',
    'use_robots_for_sitemaps',
    'active',
    'disable_ssl_verification',
    'splunk_enabled',
    'use_mobile_settings',
    'mobile_url_pattern',
    'mobile_homepage_url',
    'mobile_custom_header_user_agent',
    'mobile_custom_header_user_agent_short',
    'logzio_enabled',
    'use_renderer',
    'renderer_block_ads',
    'renderer_block_analytics',
    'renderer_block_custom',
    'renderer_js_string',
    'renderer_js_urls',
    'use_optimus',
    'is_meridian'
)

settings_immutable_fields = (

)

settings_fields = settings_mutable_fields + settings_immutable_fields


class ProjectSettings(ImmutableAttributesMixin):
    """
    Project settings class
    """
    __slots__ = settings_fields

    mutable_attributes = settings_mutable_fields

    def __init__(self, project_settings):
        self.alert_emails = project_settings.get('alert_emails')
        self.alert_setting = project_settings.get('alert_setting')
        self.api_callback = project_settings.get('api_callback')
        self.api_callback_headers = project_settings.get('api_callback_headers')
        self.attach_pdf = project_settings.get('attach_pdf')
        self.auto_finalize = project_settings.get('auto_finalize')
        self.clean_custom_extraction = project_settings.get('clean_custom_extraction')
        self.compare_to = project_settings.get('compare_to')
        self.crawl_amphtml_ext = project_settings.get('crawl_amphtml_ext')
        self.crawl_amphtml_int = project_settings.get('crawl_amphtml_int')
        self.crawl_canonicals_ext = project_settings.get('crawl_canonicals_ext')
        self.crawl_canonicals_int = project_settings.get('crawl_canonicals_int')
        self.crawl_hyperlinks_ext = project_settings.get('crawl_hyperlinks_ext')
        self.crawl_hyperlinks_int = project_settings.get('crawl_hyperlinks_int')
        self.crawl_hreflangs_ext = project_settings.get('crawl_hreflangs_ext')
        self.crawl_hreflangs_int = project_settings.get('crawl_hreflangs_int')
        self.crawl_images_ext = project_settings.get('crawl_images_ext')
        self.crawl_images_int = project_settings.get('crawl_images_int')
        self.crawl_media_mobile_ext = project_settings.get('crawl_media_mobile_ext')
        self.crawl_media_mobile_int = project_settings.get('crawl_media_mobile_int')
        self.crawl_paginations_ext = project_settings.get('crawl_paginations_ext')
        self.crawl_paginations_int = project_settings.get('crawl_paginations_int')
        self.crawl_redirects_ext = project_settings.get('crawl_redirects_ext')
        self.crawl_redirects_int = project_settings.get('crawl_redirects_int')
        self.crawl_scripts_ext = project_settings.get('crawl_scripts_ext')
        self.crawl_scripts_int = project_settings.get('crawl_scripts_int')
        self.crawl_stylesheets_ext = project_settings.get('crawl_stylesheets_ext')
        self.crawl_stylesheets_int = project_settings.get('crawl_stylesheets_int')
        self.crawl_disallow_1st_level = project_settings.get('crawl_disallow_1st_level')
        self.crawl_not_included_1st_level = project_settings.get('crawl_not_included_1st_level')
        self.crawl_nofollow = project_settings.get('crawl_nofollow')
        self.crawl_noindex = project_settings.get('crawl_noindex')
        self.crawl_non_html = project_settings.get('crawl_non_html')
        self.crawl_css_js = project_settings.get('crawl_css_js')
        self.crawl_disallowed_pages = project_settings.get('crawl_disallowed_pages')
        self.crawl_external_urls = project_settings.get('crawl_external_urls')
        self.crawl_nofollow_links = project_settings.get('crawl_nofollow_links')
        self.crawl_noindex_pages = project_settings.get('crawl_noindex_pages')
        self.crawl_non_html_file_types = project_settings.get('crawl_non_html_file_types')
        self.crawl_not_included_urls = project_settings.get('crawl_not_included_urls')
        self.crawl_rate = project_settings.get('crawl_rate')
        self.crawl_rate_advanced = project_settings.get('crawl_rate_advanced')
        self.crawl_subdomains = project_settings.get('crawl_subdomains')
        self.crawl_http_and_https = project_settings.get('crawl_http_and_https')
        self.crawl_test_site = project_settings.get('crawl_test_site')
        self.crawl_types = project_settings.get('crawl_types')
        self.custom_dns = project_settings.get('custom_dns')
        self.custom_header_user_agent = project_settings.get('custom_header_user_agent')
        self.custom_header_user_agent_short = project_settings.get('custom_header_user_agent_short')
        self.is_stealth_mode = project_settings.get('is_stealth_mode')
        self.deepcrawl_bot_url = project_settings.get('deepcrawl_bot_url')
        self.duplicate_precision = project_settings.get('duplicate_precision')
        self.low_log_summary_requests = project_settings.get('low_log_summary_requests')
        self.high_log_summary_requests = project_settings.get('high_log_summary_requests')
        self.limit_levels_max = project_settings.get('limit_levels_max')
        self.limit_pages_max = project_settings.get('limit_pages_max')
        self.location = project_settings.get('location')
        self.max_content_size = project_settings.get('max_content_size')
        self.max_description_length = project_settings.get('max_description_length')
        self.max_external_links = project_settings.get('max_external_links')
        self.max_html_size = project_settings.get('max_html_size')
        self.max_links = project_settings.get('max_links')
        self.max_load_time = project_settings.get('max_load_time')
        self.max_redirections = project_settings.get('max_redirections')
        self.max_title_width = project_settings.get('max_title_width')
        self.max_url_length = project_settings.get('max_url_length')
        self.min_content_ratio = project_settings.get('min_content_ratio')
        self.thin_page_threshold = project_settings.get('thin_page_threshold')
        self.min_description_length = project_settings.get('min_description_length')
        self.min_title_length = project_settings.get('min_title_length')
        self.empty_page_threshold = project_settings.get('empty_page_threshold')
        self.name = project_settings.get('name')
        self.page_groupings = project_settings.get('page_groupings')
        self.robots_overwrite = project_settings.get('robots_overwrite')
        self.site_primary = project_settings.get('site_primary')
        self.site_secondaries = project_settings.get('site_secondaries')
        self.site_test = project_settings.get('site_test')
        self.site_test_pass = project_settings.get('site_test_pass')
        self.site_test_user = project_settings.get('site_test_user')
        self.start_urls = project_settings.get('start_urls')
        self.url_rewrite_query_parameters = project_settings.get('url_rewrite_query_parameters')
        self.url_rewrite_regex_parameters = project_settings.get('url_rewrite_regex_parameters')
        self.url_rewrite_strip_fragment = project_settings.get('url_rewrite_strip_fragment')
        self.urls_excluded = project_settings.get('urls_excluded')
        self.urls_included = project_settings.get('urls_included')
        self.use_rewrite_rules = project_settings.get('use_rewrite_rules')
        self.use_robots_overwrite = project_settings.get('use_robots_overwrite')
        self.user_agent = project_settings.get('user_agent')
        self.mobile_user_agent = project_settings.get('mobile_user_agent')
        self.use_robots_for_sitemaps = project_settings.get('use_robots_for_sitemaps')
        self.active = project_settings.get('active')
        self.disable_ssl_verification = project_settings.get('disable_ssl_verification')
        self.splunk_enabled = project_settings.get('splunk_enabled')
        self.use_mobile_settings = project_settings.get('use_mobile_settings')
        self.mobile_url_pattern = project_settings.get('mobile_url_pattern')
        self.mobile_homepage_url = project_settings.get('mobile_homepage_url')
        self.mobile_custom_header_user_agent = project_settings.get('mobile_custom_header_user_agent')
        self.mobile_custom_header_user_agent_short = project_settings.get('mobile_custom_header_user_agent_short')
        self.logzio_enabled = project_settings.get('logzio_enabled')
        self.use_renderer = project_settings.get('use_renderer')
        self.renderer_block_ads = project_settings.get('renderer_block_ads')
        self.renderer_block_analytics = project_settings.get('renderer_block_analytics')
        self.renderer_block_custom = project_settings.get('renderer_block_custom')
        self.renderer_js_string = project_settings.get('renderer_js_string')
        self.renderer_js_urls = project_settings.get('renderer_js_urls')
        self.use_optimus = project_settings.get('use_optimus')
        self.is_meridian = project_settings.get('is_meridian')

        super(ProjectSettings, self).__init__()

    @property
    def to_dict_mutable_fields(self):
        """
        :return: dictionary with the mutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in settings_mutable_fields}

    @property
    def to_dict_immutable_fields(self):
        """
        :return: dictionary with the immutable fields
        :rtype: dict
        """
        return {x: getattr(self, x, None) for x in settings_immutable_fields}
