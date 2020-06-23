import copy
import json
import unittest
import requests
import six
import os
import re
from PIL import Image
from functools import reduce
from abc import abstractmethod, ABCMeta
from sumoappclient.omnistorage.factory import ProviderFactory
from sumoapputils.common.utils import EXCLUDED_APPS_WITHOUT_SC_PARAMS, get_test_logger

try:
    from sumoapputils.appdev.appdeployapi import push_app_api, push_app_api_v2
except ImportError:
    raise Exception("push_app_api, push_app_api_v2 functions are not available")

logger = get_test_logger()


@six.add_metaclass(ABCMeta)
class TestApp(unittest.TestCase):

    COMMUNITY_URL = "https://support.sumologic.com/hc/en-us/community/topics/200263058-Applications-and-Integrations"
    MAX_FILE_SIZE = 5*1000*1000
    CUMULATIVE_MAX_FILE_SIZE = 100*1000*1000

    def __init__(self, manifestfile, appfile, deployment_name,
                 access_id, access_key, *args, **kwargs):
        super(TestApp, self).__init__(*args, **kwargs)
        self.HELP_HOME_URL = "https://help.sumologic.com/"
        self.S3_URL_PREFIX = "https://s3.amazonaws.com/"
        self.ICON_URL_PREFIX = ("https://app_icons.s3.amazonaws.com", self.S3_URL_PREFIX, "https://sumologic-partner-appsdata.s3.amazonaws.com")
        self.SCREENSHOT_URL_PREFIX = ("https://sumologic-app-data.s3.amazonaws.com", self.S3_URL_PREFIX, "https://sumologic-partner-appsdata.s3.amazonaws.com")
        self.HARDCODED_PARAM_APPS = ("InternalVolume", "Audit", "Artifactory", "Enterprise_Audit_Collector_Data_Forwarding", "Enterprise_Audit_Content_Management", "Enterprise_Audit_Security_Management", "Enterprise_Audit_User_role_Management")
        self.manifestfile = manifestfile
        self.appfile = appfile
        self.deployment_name = deployment_name
        self.access_id = access_id
        self.access_key = access_key
        self.appjson = self.get_valid_json(self.appfile)
        self.manifestjson = self.get_valid_json(self.manifestfile)
        self.foldername = os.path.basename(os.path.dirname(appfile))
        try:
            self.app_description = self.manifestjson["description"]
            self.app_parameters = self.manifestjson["parameters"]
            self.app_preview_status = self.manifestjson["preview"]
            self.app_version = self.manifestjson["version"]
            self.appname = self.manifestjson["name"]
            self.dashboards, self.searches = self.get_content(self.appjson)
            self.remove_text_panels(self.dashboards)
            self.queryparams = ["$$%s" % param["parameterId"] for param in self.app_parameters  if param['dataSourceType'] == "LOG" or param['dataSourceType'] == "METRICS"]
            self.log_queries, self.metric_queries = self.extract_queries(self.dashboards)
            self.saved_search_queries = self.get_saved_search_queries(self.searches)
        except KeyError as e:
            raise Exception("%s: InitError: Required Params %s are missing from json " % (self.appname, e))

    @classmethod
    def extract_queries(self, dashboards):
        log_queries = []
        metric_queries = []
        for dash in dashboards:
            dash_name = dash.get("name")
            if self.is_mew_board(dash):
                for panel in dash["rootPanel"]["panels"]:
                    if panel.get("panelType") == "TextPanel" or panel.get("Type") == "TextPanel":
                        continue
                    for query in panel["queries"]:
                        panel_name = panel.get("title")
                        if query["queryType"] == "Logs":
                            log_queries.append((query["queryString"], panel_name, dash_name))
                        else:
                            metric_queries.append((query["queryString"], panel_name, dash_name))
            else:
                for panel in dash["panels"]:
                    if panel["viewerType"] in ("title", "text"):
                        continue
                    panel_name = panel.get("name")
                    if (panel["queryString"] != ""):
                        log_queries.append((panel["queryString"], panel_name, dash_name))
                    else:
                        for mquery in panel["metricsQueries"]:
                            metric_queries.append((mquery["query"], panel_name, dash_name))

        return log_queries, metric_queries

    @abstractmethod
    def get_saved_search_queries(self, searches):
        raise NotImplementedError()

    @abstractmethod
    def get_content(self, folder):
        raise NotImplementedError()

    @abstractmethod
    def remove_text_panels(self, dashboards):
        raise NotImplementedError()

    def setUp(self):
        self.warnings = []
        self.test_name = self.id().split(".")[-1]

    def add_warning(self, msg):
        self.warnings.append((self, msg))

    def run(self, result):
        obj = super(TestApp, self).run(result)
        result.appname = self.appname
        result.warnings.extend(self.warnings)
        return obj

    @classmethod
    def get_valid_json(cls, filepath):
        appjson = None
        try:
            with open(filepath) as fp:
                appjson = json.load(fp)
        except BaseException as e:
            raise Exception("InitError: Failed to read json %s" % e)

        return appjson

    @classmethod
    def is_mew_board(cls, dash):
        return dash["type"] in ("Dashboard", "MewboardSyncDefinition")

    @abstractmethod
    def test_is_deployable(self):
        raise NotImplementedError()

    def test_has_app_description(self):
        self.assertTrue(self.app_description != "", "App description is empty")

    def test_has_dashboard_description(self):
        err = []
        for dash in self.dashboards:
            if not dash["description"]:
                err.append(dash.get("name"))
        if err:
            msg = "No dashboard description in following dashboards %s" % (",".join(err))
            self.add_warning(msg)

    def _is_valid_url(self, url, entityname="URL"):
        resp = None
        max_try = 3
        retry = 0
        while retry < max_try:
            try:
                resp = requests.get(url)
                break
            except requests.Timeout as e:
                retry += 1
                logger.error("%s Timeout while getting url %s. retrying...%d" % (
                    self.appname, url, retry))
            except Exception as e:
                self.fail("%s: Invalid %s url: %s error: %s" % (
                    self.appname, entityname, url, e))
                break
        return resp

    def test_has_community_url(self):
        url = self.manifestjson.get("communityURL", "")
        self.assertTrue(url != "", "Community URL is empty")
        self.assertTrue(url == self.COMMUNITY_URL, "Community URL is incorrect")

    def test_has_helpdoc_url(self):
        url = self.manifestjson.get("helpURL", "")
        self.assertTrue(url != "", "HelpURL is empty")
        resp = self._is_valid_url(url, "HelpURL")
        # including this test in warning because dochub service may be down
        if hasattr(resp, "status_code"):
            msg = ""
            if resp.status_code != 200:
                msg += "Throwing %d status_code Reason: %s" % (resp.status_code, resp.reason)
            if resp.url == self.HELP_HOME_URL:
                msg += "HelpURL redirecting to Doc Home Page"
            if not re.search(self.appname, resp.content.decode('utf-8', 'ignore'), flags=re.IGNORECASE):
                msg += "Does not contains appname"
            if msg:
                self.add_warning("HelpURL: %s %s" % (url, msg))

    def test_has_category(self):
        catg = self.manifestjson.get("categories", [])
        self.assertTrue(len(catg) > 0, "No App category found")
        self.assertTrue(len(catg) <= 3, "Maximum 3 App categories allowed")

    def test_has_valid_icon(self):
        url = self.manifestjson.get("iconURL", "")
        self.assertTrue(url != "", "iconURL is empty")
        resp = self._is_valid_url(url, "IconURL")
        if hasattr(resp, "status_code"):
            self.assertTrue(resp.status_code == 200, "Icon URL throwing %d status_code Reason: %s" % (resp.status_code, resp.reason))
            self.assertTrue(url.startswith(self.ICON_URL_PREFIX),
                            "Icon URL: %s is not S3 based" % url)

    def test_has_valid_screenshots(self):
        # Todo check first should be overview
        screenshots = self.manifestjson.get("screenshotURLs", [])
        self.assertTrue(len(screenshots) > 0,
                        "Appname: %s Screenshot URLs are not present" % (self.appname))
        for url in screenshots:
            resp = self._is_valid_url(url, "Screenshot URL")
            if hasattr(resp, "status_code"):
                self.assertTrue(resp.status_code == 200, "screenshot url: %s throws status_code: %s Reason: %s" % (
                                url, resp.status_code, resp.reason))
                self.assertTrue(url.startswith(self.SCREENSHOT_URL_PREFIX),
                                "screenshot url: %s is not S3 based" % url)

    @abstractmethod
    def test_valid_timerange(self):
        raise NotImplementedError()

    def test_has_valid_dashboard_title(self):
        err = []
        for dash in self.dashboards:
            if not self.appname in dash["name"]:
                err.append(dash.get("name"))
        if err:
            msg = "Following dashboards %s should follow <appname>-<dashboard title>" % ",".join(err)
            self.add_warning(msg)


    def test_version_preview_consistent(self):
        if self.app_preview_status:
            self.assertTrue(self.app_version == "BETA", "App version should be BETA")
        else:
            self.assertTrue(float(self.app_version) > 0, "App version should be > 0")

    def test_folder_description(self):
        pass

    # def test_app_description_and_name_same_in_manifest(self):
    #     pass

    def test_folder_structure(self):
        app_dir = os.path.dirname(self.appfile)
        # folder exists
        resource_folder = os.path.join(app_dir, "resources")
        self.assertTrue(os.path.isdir(resource_folder))

        for folder_name in ["logs", "icon", "screenshots"]:
            folder = os.path.join(resource_folder, folder_name)
            self.assertTrue(os.path.isdir(folder))

            if folder_name in ["icon", "screenshots"] and os.listdir(folder) == 0:
                self.add_warning("%s folder is empty" % folder_name)

        file_size_sum = 0
        for root, dirs, files in os.walk(resource_folder):
            for filename in files:
                if " " in filename:
                    self.add_warning("Whitespace in filename: %s" % filename)
                filepath = os.path.join(root, filename)
                # non empty
                filesize = os.stat(filepath).st_size
                self.assertTrue( filesize > 0)
                parent_dir = os.path.basename(root.strip("/"))
                if parent_dir in ["icon", "screenshots"]:
                    self.assertTrue(filesize < self.MAX_FILE_SIZE)
                if parent_dir in ["screenshots"]:
                    im = Image.open(filepath)
                    width, height = im.size
                    self.assertTrue(width > 832 and height > 520, "Image dimension should be 832x520 or greater")
                    logger.info("ImageName: %s Width: %s Height: %s" % (filename, width, height))
                    if width < 1400:
                        self.add_warning("For optimal full screen size we recommend width of 1400")
                elif parent_dir == "logs":
                    self.assertTrue(filesize < 2*self.MAX_FILE_SIZE)
                file_size_sum += filesize

        self.assertTrue(file_size_sum < self.CUMULATIVE_MAX_FILE_SIZE)

    def test_uuid_matches_stored_value(self):
        op_cli = ProviderFactory.get_provider("aws")
        store = op_cli.get_storage("keyvalue", 'partner_app_ids', logger=logger)
        repo_url = os.getenv("GIT_REPO_URL", "")
        repo_full_name = repo_url.split("github.com" )[-1].strip("/").strip(":")
        self.assertTrue(self.manifestjson["uuid"] == store.get(repo_full_name))

    def check_params_in_log_query(self, query_string, location_text):
        func = lambda r, x: r or x in query_string
        has_params_in_query = reduce(func, self.queryparams, False)
        if not has_params_in_query:
            msg = "%s is not using %s" % (
                location_text, ",".join(self.queryparams))
            if self.appname in EXCLUDED_APPS_WITHOUT_SC_PARAMS:
                self.add_warning(msg)
            else:
                self.assertTrue(has_params_in_query, msg)

    def check_params_in_metric_query(self, query_string, panel_name, dash_name):
        func = lambda r, x: r or x in query_string
        has_params_in_query = reduce(func, self.queryparams, False) or '#' in query_string
        if not has_params_in_query:
            msg = "Metric Panel: %s in Dashboard: %s is not using %s" % (
                panel_name, dash_name, ",".join(self.queryparams))
            if self.appname in EXCLUDED_APPS_WITHOUT_SC_PARAMS:
                self.add_warning(msg)
            else:
                self.assertTrue(has_params_in_query, msg)

    def check_default_lookup_in_query(self, query_string, location_text):
        hasgeo = "geo://default" in query_string
        self.assertTrue(not hasgeo, "%s should use geo://location" % location_text)
        hasmetro_code = "metro_code" in query_string
        self.assertTrue(not hasmetro_code, "%s should not use metro_code" % location_text)
        hasarea_code = "area_code" in query_string
        self.assertTrue(not hasarea_code, "%s should not use area_code" % location_text)

    def check_external_lookups(self, query_string, location_text):
        SUMO_LOOKUPS = {"geo://location", "geo://default", "sumo://threat/cs"}
        lookup_regex = r'\s+lookup\s+[\w,\s]+?from\s+(?P<source>.*?)\s+(?=on\s+)'
        matched = re.findall(lookup_regex, query_string, flags=re.IGNORECASE)
        if matched:
            for source in matched:
                if source not in SUMO_LOOKUPS:
                    msg = "%s is using external lookup %s" % (location_text, source)
                    self.add_warning(msg)

    def check_save_operator(self, query_string, location_text):
        saved_regex = r'\s+save\s+(?:append\s+)?(?P<source>.*?)\s?'
        matched = re.findall(saved_regex, query_string, flags=re.IGNORECASE)
        if matched:
            for source in matched:
                msg = "%s is using save operator with file %s" % (location_text, source)
                self.add_warning(msg)

    def test_all_params_replaced_in_dashboards(self):
        # apps having hardcoded params
        if self.foldername in self.HARDCODED_PARAM_APPS:
            return
        logger.warning("These tests do not cover multiple metadata(_sourceCategories,_source etc). They may or may not be replaced")

        for query_string, panel_name, dash_name in self.log_queries:
            self.check_params_in_log_query(query_string, "Log Panel: %s in Dashboard: %s" % (panel_name, dash_name))

        for query_string, panel_name, dash_name in self.metric_queries:
            self.check_params_in_metric_query(query_string, panel_name, dash_name)

        # for saved searches
        for query_string, search_name in self.saved_search_queries:
            self.check_params_in_log_query(query_string, "SavedSearch %s:" % search_name)

    def test_not_using_default_lookup(self):
        for query_string, panel_name, dash_name in self.log_queries:
            self.check_default_lookup_in_query(query_string, "Panel: %s in Dashboard: %s" % (panel_name, dash_name))

        for query_string, search_name in self.saved_search_queries:
            self.check_default_lookup_in_query(query_string, "SavedSearch: %s" % search_name)

    def test_has_lookup_operator_from_external_files(self):

        for query_string, panel_name, dash_name in self.log_queries:
            self.check_external_lookups(query_string, "Panel: %s in Dashboard: %s" % (panel_name, dash_name))

        for query_string, search_name in self.saved_search_queries:
            self.check_external_lookups(query_string, "SavedSearch: %s" % search_name)

    def test_has_save_operator(self):

        for query_string, panel_name, dash_name in self.log_queries:
            self.check_save_operator(query_string, "Log Panel: %s in Dashboard: %s" % (panel_name, dash_name))

        for query_string, search_name in self.saved_search_queries:
            self.check_save_operator(query_string, "SavedSearch: %s" % search_name)

    @abstractmethod
    def test_has_scheduled_searches(self):
        raise NotImplementedError

    @classmethod
    def order_dashboards_by_name(cls, dashboards):
        dashboards = copy.deepcopy(dashboards)
        dashboards = sorted(dashboards, key=lambda x: x.get("name"))
        return dashboards

    @classmethod
    def order_panels_by_name(cls, dashboards):
        dashboards = copy.deepcopy(dashboards)
        for dash in dashboards:
            if cls.is_mew_board(dash):
                if "rootPanel" in dash and "panels" in dash["rootPanel"]:
                    dash["rootPanel"]["panels"] = sorted(dash["rootPanel"]["panels"], key=lambda x: x.get("title"))
            elif "panels" in dash:
                dash["panels"] = sorted(dash["panels"], key=lambda x: x.get("name"))

        return dashboards

    @classmethod
    def order_searches_by_name(cls, searches):
        searches = copy.deepcopy(searches)
        searches = sorted(searches, key=lambda x: x.get("name"))
        return searches


class TestClassicDashboards(TestApp):

    @classmethod
    def remove_text_panels(self, dashboards):
        for dash in dashboards:
            if self.is_mew_board(dash):
                dash["rootPanel"]["panels"] = [panel for panel in dash["rootPanel"]["panels"] if not (panel["type"] in ("TextPanel"))]
            else:
                dash["panels"] = [panel for panel in dash["panels"] if not (panel["viewerType"] in ("title", "text"))]

    @classmethod
    def get_content(self, folder):
        searches = []
        dashboards = []
        for dash in folder["children"]:
            if dash["type"] in ("Report", "Dashboard"):
                dashboards.append(dash)
            elif dash["type"] == "Search":
                searches.append(dash)
            elif dash["type"] == "Folder":
                d, s = self.get_content(dash)
                searches.extend(s)
                dashboards.extend(d)
        return dashboards, searches

    @classmethod
    def get_saved_search_queries(self, searches):
        search_queries = []
        for search in searches:
            search_queries.append((search["searchQuery"], search["name"]))
        return search_queries


    def test_is_deployable(self):
        status, response = push_app_api(self.deployment_name, self.appfile, self.manifestfile, self.access_id, self.access_key)
        self.assertTrue("succeeded" in str(response).lower(),
                        "Unable to deploy app on deployment: %s response: %s" % (
                         self.deployment_name, response))

    def test_valid_timerange(self):
        for dash in self.dashboards:
            if self.is_mew_board(dash):
                for panel in dash["rootPanel"]["panels"]:
                    self.assertTrue("timeRange" not in panel or panel["timeRange"] is None or "relative" in json.dumps(panel["timeRange"]),
                                    "Panel: %s in Dashboard: %s does not use relative time" % (
                                        panel.get("title"), dash.get("name")))
            else:
                for panel in dash["panels"]:
                    self.assertTrue("relative" in panel["timeRange"],
                                    "Panel: %s in Dashboard: %s does not use relative time" % (
                                    panel.get("name"), dash.get("name")))

        # Todo check time range for scheduled searches

    def test_has_scheduled_searches(self):
        for search in self.searches:
            if "schedules" in search:
                self.add_warning("SavedSearch %s is scheduled with type %s" % (search['name'], search["schedules"]['notification']['type']))


class TestClassicDashboardsV2(TestApp):

    @classmethod
    def remove_text_panels(self, dashboards):
        for dash in dashboards:
            if self.is_mew_board(dash):
                dash["rootPanel"]["panels"] = [panel for panel in dash["rootPanel"]["panels"] if not (panel["panelType"] in ("TextPanel"))]
            else:
                dash["panels"] = [panel for panel in dash["panels"] if not (panel["viewerType"] in ("title", "text"))]

    @classmethod
    def get_content(self, folder):
        searches = []
        dashboards = []
        for dash in folder["children"]:
            if dash["type"] in ("DashboardSyncDefinition", "MewboardSyncDefinition"):
                dashboards.append(dash)
            elif dash["type"] == "SavedSearchWithScheduleSyncDefinition":
                searches.append(dash)
            elif dash["type"] == "FolderSyncDefinition":
                d, s = self.get_content(dash)
                searches.extend(s)
                dashboards.extend(d)
        return dashboards, searches

    def test_is_deployable(self):
        status, response = push_app_api_v2(self.deployment_name, self.appfile, self.manifestfile, self.access_id, self.access_key)
        self.assertTrue("success" in str(response).lower(),
                        "Unable to deploy app on deployment: %s response: %s" % (
                         self.deployment_name, response))

    def test_valid_timerange(self):
        for dash in self.dashboards:
            if self.is_mew_board(dash):
                for panel in dash["rootPanel"]["panels"]:
                    self.assertTrue("timeRange" not in panel or panel["timeRange"] is None or "relative" in json.dumps(panel["timeRange"]),
                                    "Panel: %s in Dashboard: %s does not use relative time" % (
                                        panel.get("title"), dash.get("name")))
            else:
                for panel in dash["panels"]:
                    timerangestr = json.dumps(panel["timeRange"])
                    self.assertTrue("RelativeTimeRangeBoundary" in timerangestr or "CompleteLiteralTimeRange" in timerangestr, "Panel: %s in Dashboard: %s does not use relative time" % (
                        panel.get("name"), dash.get("name")))
        # Todo check time range for scheduled searches

    @classmethod
    def get_saved_search_queries(self, searches):
        search_queries = []
        for search in searches:
            search_queries.append((search['search']["queryText"], search["name"]))
        return search_queries

    def test_has_scheduled_searches(self):
        for search in self.searches:
            if "searchSchedule" in search and search["searchSchedule"]:
                self.add_warning("SavedSearch %s is scheduled with type %s" % (search['name'], search['searchSchedule']['notification']['taskType']))
