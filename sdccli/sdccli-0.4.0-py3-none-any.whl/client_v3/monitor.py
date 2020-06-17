import requests
import json
import tatsu
import copy
from sdcclient import SdMonitorClient as MonitorClient


class SdMonitorClient(MonitorClient):
    def __init__(self, token="", sdc_url='https://app.sysdigcloud.com', ssl_verify=True, custom_headers=None):
        super(SdMonitorClient, self).__init__(token, sdc_url, ssl_verify, custom_headers)
        self.product = "SDC"
        self._dashboards_api_version = 'v3'
        self._dashboards_api_endpoint = '/api/{}/dashboards'.format(self._dashboards_api_version)
        self._default_dashboards_api_endpoint = '/api/{}/defaultDashboards'.format(self._dashboards_api_version)

    def get_dashboards(self):
        '''**Description**
            Return the list of dashboards available under the given user account. This includes the dashboards created by the user and the ones shared with her by other users.

        **Success Return Value**
            A dictionary containing the list of available sampling intervals.

        **Example**
            `examples/list_dashboards.py <https://github.com/draios/python-sdc-client/blob/master/examples/list_dashboards.py>`_
        '''
        res = requests.get(self.url + self._dashboards_api_endpoint, params={"light": "true"}, headers=self.hdrs,
                           verify=self.ssl_verify)
        return self._request_result(res)

    def create_dashboard(self, name):
        '''
        **Description**
            Creates an empty dashboard. You can then add panels by using ``add_dashboard_panel``.

        **Arguments**
            - **name**: the name of the dashboard that will be created.

        **Success Return Value**
            A dictionary showing the details of the new dashboard.

        **Example**
            `examples/dashboard.py <https://github.com/draios/python-sdc-client/blob/master/examples/dashboard.py>`_
        '''
        dashboard_configuration = {
            'name': name,
            'schema': 3,
            'widgets': [],
            'eventsOverlaySettings': {
                'filterNotificationsUserInputFilter': ''
            },
            'layout': [],
            'panels': [],
        }

        #
        # Create the new dashboard
        #
        res = requests.post(self.url + self._dashboards_api_endpoint, headers=self.hdrs,
                            data=json.dumps({'dashboard': dashboard_configuration}),
                            verify=self.ssl_verify)
        return self._request_result(res)

    def create_dashboard_from_file(self, dashboard_name, filename, filter=None, shared=False, public=False):
        '''
        **Description**
            Create a new dasboard using a dashboard template saved to disk. See :func:`~SdcClient.save_dashboard_to_file` to use the file to create a dashboard (usefl to create and restore backups).

            The file can contain the following JSON formats:
            1. dashboard object in the format of an array element returned by :func:`~SdcClient.get_dashboards`
            2. JSON object with the following properties:
                * version: dashboards API version (e.g. 'v2')
                * dashboard: dashboard object in the format of an array element returned by :func:`~SdcClient.get_dashboards`

        **Arguments**
            - **dashboard_name**: the name of the dashboard that will be created.
            - **filename**: name of a file containing a JSON object
            - **filter**: a boolean expression combining Sysdig Monitor segmentation criteria defines what the new dasboard will be applied to. For example: *kubernetes.namespace.name='production' and container.image='nginx'*.
            - **shared**: if set to True, the new dashboard will be a shared one.
            - **public**: if set to True, the new dashboard will be shared with public token.

        **Success Return Value**
            A dictionary showing the details of the new dashboard.

        **Example**
            `examples/dashboard_save_load.py <https://github.com/draios/python-sdc-client/blob/master/examples/dashboard_save_load.py>`_
        '''
        #
        # Load the Dashboard
        #
        with open(filename) as data_file:
            loaded_object = json.load(data_file)

        #
        # Handle old files
        #
        if 'dashboard' not in loaded_object:
            loaded_object = {
                'version': f'v{loaded_object["schema"]}',
                'dashboard': loaded_object
            }

        dashboard = loaded_object['dashboard']

        if loaded_object['version'] != self._dashboards_api_version:
            #
            # Convert the dashboard (if possible)
            #
            conversion_result, dashboard = self._convert_dashboard_to_current_version(dashboard,
                                                                                      loaded_object['version'])

            if conversion_result == False:
                return conversion_result, dashboard

        #
        # Create the new dashboard
        #
        return self.create_dashboard_from_template(dashboard_name, dashboard, filter, shared, public)

    def create_dashboard_from_template(self, dashboard_name, template, scope=None, shared=False, public=False):
        if scope is not None:
            if not isinstance(scope, list):
                return [False, 'Invalid scope format: Expected a list or None']
        else:
            scope = []

        #
        # Clean up the dashboard we retireved so it's ready to be pushed
        #
        template['id'] = None
        template['version'] = None
        template['schema'] = 3
        template['name'] = dashboard_name
        template['shared'] = shared
        template['public'] = public
        template['publicToken'] = None

        # default dashboards don't have eventsOverlaySettings property
        # make sure to add the default set if the template doesn't include it
        if 'eventsOverlaySettings' not in template or not template['eventsOverlaySettings']:
            template['eventsOverlaySettings'] = {
                'filterNotificationsUserInputFilter': ''
            }

        # set dashboard scope to the specific parameter
        template['scopeExpressionList'] = []
        for s in scope:
            ok, converted_scope = self.convert_scope_string_to_expression(s)
            if not ok:
                return converted_scope
            template['scopeExpressionList'].append(converted_scope)

        # NOTE: Individual panels might override the dashboard scope, the override will NOT be reset
        if 'widgets' in template and template['widgets'] is not None:
            for chart in template['widgets']:
                if 'overrideScope' not in chart:
                    chart['overrideScope'] = False

                if chart['overrideScope'] == False:
                    # patch frontend bug to hide scope override warning even when it's not really overridden
                    chart['scope'] = scope

                if chart['showAs'] != 'map':
                    # if chart scope is equal to dashboard scope, set it as non override
                    chart_scope = chart['scope'] if 'scope' in chart else None
                    chart['overrideScope'] = chart_scope != scope
                else:
                    # topology panels must override the scope
                    chart['overrideScope'] = True

        #
        # Create the new dashboard
        #
        res = requests.post(self.url + self._dashboards_api_endpoint, headers=self.hdrs,
                            data=json.dumps({'dashboard': template}), verify=self.ssl_verify)

        return self._request_result(res)

    def create_dashboard_from_dashboard(self, newdashname, templatename, filter=None, shared=False, public=False):
        '''**Description**
            Create a new dasboard using one of the existing dashboards as a template. You will be able to define the scope of the new dasboard.

        **Arguments**
            - **newdashname**: the name of the dashboard that will be created.
            - **viewname**: the name of the dasboard to use as the template, as it appears in the Sysdig Monitor dashboard page.
            - **filter**: a boolean expression combining Sysdig Monitor segmentation criteria defines what the new dasboard will be applied to. For example: *kubernetes.namespace.name='production' and container.image='nginx'*.
            - **shared**: if set to True, the new dashboard will be a shared one.
            - **public**: if set to True, the new dashboard will be shared with public token.

        **Success Return Value**
            A dictionary showing the details of the new dashboard.

        **Example**
            `examples/create_dashboard.py <https://github.com/draios/python-sdc-client/blob/master/examples/create_dashboard.py>`_
        '''
        #
        # Get the list of dashboards from the server
        #
        dashboard = requests.get(self.url + self._dashboards_api_endpoint, params={"light": "true"}, headers=self.hdrs,
                                 verify=self.ssl_verify)
        if not self._checkResponse(dashboard):
            return [False, self.lasterr]

        j = dashboard.json()

        #
        # Find our template dashboard
        #
        dboard = None

        for db in j['dashboards']:
            if db['name'] == templatename:
                dboard = db
                break

        if dboard is None:
            self.lasterr = 'can\'t find dashboard ' + templatename + ' to use as a template'
            return [False, self.lasterr]

        ok, dboard = self.get_dashboard(dboard["id"])
        if not ok:
            return ok, dboard
        #
        # Create the dashboard
        #
        return self.create_dashboard_from_template(newdashname, dboard["dashboard"], filter, shared, public)

    def favorite_dashboard(self, dashboard_id, favorite):
        data = {"dashboard": {"favorite": favorite}}
        res = requests.patch(self.url + self._dashboards_api_endpoint + "/" + str(dashboard_id), json=data,
                             headers=self.hdrs, verify=self.ssl_verify)
        return self._request_result(res)

    @staticmethod
    def convert_scope_string_to_expression(scope):
        _SCOPE_GRAMMAR = """
            @@grammar::CALC

            start = expression $ ;

            expression 
                = 
                |   operand simple_operator word
                |   operand multiple_operator multiple_value
                ;

            simple_operator
                =
                |  'is not'
                |  'is'
                |  'contains'
                |  'does not contain'
                |  'starts with'
                ;

            multiple_operator
                =
                |  'not in'
                |  'in'
                ;

            operand = /[\w\.]+/ ;

            multiple_value 
                = 
                | '[' word_array ']'
                | word
                ;

            word_array
                =
                | word ',' word_array
                | word
                ;

            word = /[\w\.]+/ ;
        """

        def flatten(S):
            if S == [] or S == ():
                return list(S)
            if isinstance(S[0], list) or isinstance(S[0], tuple):
                return flatten(S[0]) + flatten(S[1:])
            return list(S[:1]) + flatten(S[1:])

        try:
            grammar = tatsu.compile(_SCOPE_GRAMMAR)

            operand, parsed_operator, value = grammar.parse(scope)

            operator_match = {
                "is": "equals",
                "is not": "notEquals",
                "in": "in",
                "not in": "notIn",
                "contains": "contains",
                "does not contain": "notContains",
                "starts with": "startsWith",
            }

            if isinstance(value, tuple):
                value = flatten(value)
                if len(value) > 1:
                    value = list(value[1:-1])  # Remove '[' and ']'
                    value = [elem for elem in value if elem != ',']  # Remove ','
            else:
                value = [value]

            operator = "" if parsed_operator not in operator_match else operator_match[parsed_operator]

            return [True, {
                'displayName': "",
                "isVariable": False,
                'operand': operand,
                'operator': operator,
                'value': value
            }]
        except Exception as ex:
            return [False, f"invalid scope: {scope}, {ex.message}"]

    def share_dashboard_with_all_teams(self, dashboard, mode="r"):
        role = "ROLE_RESOURCE_READ" if mode == "r" else "ROLE_RESOURCE_EDIT"
        dboard = copy.deepcopy(dashboard)
        dboard["sharingSettings"] = [
            {
                "member": {
                    "type": "USER_TEAMS",
                },
                "role": role,
            }
        ]
        dboard["shared"] = True

        return self.update_dashboard(dboard)

    def unshare_dashboard(self, dashboard):
        dboard = copy.deepcopy(dashboard)
        dboard["sharingSettings"] = []
        dboard["shared"] = False

        return self.update_dashboard(dboard)

    def share_dashboard_with_team(self, dashboard, team_id, mode="r"):
        role = "ROLE_RESOURCE_READ" if mode == "r" else "ROLE_RESOURCE_EDIT"
        dboard = copy.deepcopy(dashboard)

        if dboard["sharingSettings"] == None:
            dboard["sharingSettings"] = []

        dboard["sharingSettings"].append({
            "member": {
                "type": "TEAM",
                "id": team_id,
            },
            "role": role,
        })
        dboard["shared"] = True

        return self.update_dashboard(dboard)

    def create_alert(self, name=None, description=None, severity=None, for_atleast_s=None, condition=None,
                     segmentby=[], segment_condition='ANY', user_filter='', notify=None, enabled=True,
                     annotations={}, alert_obj=None, type="MANUAL"):
        '''**Description**
            Create a threshold-based alert.

        **Arguments**
            - **name**: the alert name. This will appear in the Sysdig Monitor UI and in notification emails.
            - **description**: the alert description. This will appear in the Sysdig Monitor UI and in notification emails.
            - **severity**: syslog-encoded alert severity. This is a number from 0 to 7 where 0 means 'emergency' and 7 is 'debug'.
            - **for_atleast_s**: the number of consecutive seconds the condition must be satisfied for the alert to fire.
            - **condition**: the alert condition, as described here https://app.sysdigcloud.com/apidocs/#!/Alerts/post_api_alerts
            - **segmentby**: a list of Sysdig Monitor segmentation criteria that can be used to apply the alert to multiple entities. For example, segmenting a CPU alert by ['host.mac', 'proc.name'] allows to apply it to any process in any machine.
            - **segment_condition**: When *segmentby* is specified (and therefore the alert will cover multiple entities) this field is used to determine when it will fire. In particular, you have two options for *segment_condition*: **ANY** (the alert will fire when at least one of the monitored entities satisfies the condition) and **ALL** (the alert will fire when all of the monitored entities satisfy the condition).
            - **user_filter**: a boolean expression combining Sysdig Monitor segmentation criteria that makes it possible to reduce the scope of the alert. For example: *kubernetes.namespace.name='production' and container.image='nginx'*.
            - **notify**: the type of notification you want this alert to generate. Options are *EMAIL*, *SNS*, *PAGER_DUTY*, *SYSDIG_DUMP*.
            - **enabled**: if True, the alert will be enabled when created.
            - **annotations**: an optional dictionary of custom properties that you can associate to this alert for automation or management reasons
            - **alert_obj**: an optional fully-formed Alert object of the format returned in an "alerts" list by :func:`~SdcClient.get_alerts` This is an alternative to creating the Alert using the individual parameters listed above.

        **Success Return Value**
            A dictionary describing the just created alert, with the format described at `this link <https://app.sysdigcloud.com/apidocs/#!/Alerts/post_api_alerts>`__

        **Example**
            `examples/create_alert.py <https://github.com/draios/python-sdc-client/blob/master/examples/create_alert.py>`_
        '''
        #
        # Get the list of alerts from the server
        #
        res = requests.get(self.url + '/api/alerts', headers=self.hdrs, verify=self.ssl_verify)
        if not self._checkResponse(res):
            return [False, self.lasterr]
        res.json()

        if alert_obj is None:
            if None in (name, description, severity, for_atleast_s, condition):
                return [False, 'Must specify a full Alert object or all parameters: name, description, severity, for_atleast_s, condition']
            else:
                #
                # Populate the alert information
                #
                alert_json = {
                    'alert': {
                        'type': type,
                        'name': name,
                        'description': description,
                        'enabled': enabled,
                        'severity': severity,
                        'timespan': for_atleast_s * 1000000,
                        'condition': condition,
                        'filter': user_filter
                    }
                }

                if segmentby != None and segmentby != []:
                    alert_json['alert']['segmentBy'] = segmentby
                    alert_json['alert']['segmentCondition'] = {'type': segment_condition}

                if annotations != None and annotations != {}:
                    alert_json['alert']['annotations'] = annotations

                if notify != None:
                    alert_json['alert']['notificationChannelIds'] = notify
        else:
            # The REST API enforces "Alert ID and version must be null", so remove them if present,
            # since these would have been there in a dump from the list_alerts.py example.
            alert_obj.pop('id', None)
            alert_obj.pop('version', None)
            alert_json = {
                'alert': alert_obj
            }

        #
        # Create the new alert
        #
        res = requests.post(self.url + '/api/alerts', headers=self.hdrs, data=json.dumps(alert_json), verify=self.ssl_verify)
        return self._request_result(res)