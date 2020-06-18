# Set up the token-based API calls by first getting the Auth Token
import configparser,json,requests,os,urllib3,sys,argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def m(method):
    return method.strip().lower()


""" Decorators for Http Request Handlers """
def POST(func):
    """ POST function decorator """
    def wrapper(*args,**kw):
        endpoint,method = args[1],args[2]
        if m(method) != "post":
            print("{} only accepts POST requests".format(endpoint))
            print("You attempted {}".format(method))
            sys.exit(1)
        else:
            return func(*args,**kw)
    return wrapper
def GET(func):
    """ GET function decorator """
    def wrapper(*args,**kw):
        endpoint,method = args[1],args[2]
        if m(method) != "get":
            print("{} only accepts GET requests".format(endpoint))
            print("You attempted {}".format(method))
            sys.exit(1)
        else:
            return func(*args,**kw)
    return wrapper
def PUT(func):
    """ PUT function decorator """
    def wrapper(*args,**kw):
        endpoint,method = args[1],args[2]
        if m(method) != "put":
            print("{} only accepts PUT requests".format(endpoint))
            print("You attempted {}".format(method))
            sys.exit(1)
        else:
            return func(*args,**kw)
    return wrapper

def DELETE(func):
    """ DELETE function decorator """
    def wrapper(*args,**kw):
        endpoint,method = args[1],args[2]
        if m(method) != "delete":
            print("{} only accepts DELETE requests".format(endpoint))
            print("You attempted {}".format(method))
            sys.exit(1)
        else:
            return func(*args,**kw)
    return wrapper



# Pull config from config.ini
class StatusCastAPIDriver:
    def __init__(self):
        """ Constructor for StatusCastAPIDriver. You need to call .initialize_session() on this object after
        creation, passing username (str),password (str),base_url (str),and verify_ssl (boolean) to that method
        to create an authenticated API session. """
        self.username = ""
        self.password = ""
        self.base_url = ""
        self.verify_ssl = False
        self.session_initialized = False

    def __str__(self):
        if self.session_initialized:
            msg = "StatusCastAPIDriver object with an initialized session, with " \
                "username={},base_url={},verify_ssl={},password={}".format(
                    self.username,self.base_url,self.verify_ssl,self.password
                )
        else:
            msg = "StatusCastAPIDriver object without an initialized session"
        return msg

    def initialize_session(self, password="",username="",base_url="",verify_ssl=False):
        """
        Initialize an authorized session using username/password/base_url/verify_ssl args
        by getting a token and updating session headers with that token
        """
        if username == "":
            print("You must provide a valid value for username, ({} is not a valid value)".format(username))
            print("Alternatively, provide ")
            sys.exit(1)
        elif password == "":
            print("You must provide a valid value for password, ({} is not a valid value)".format(password))
            sys.exit(1)
        elif base_url == "":
            print("You must provide a valid value for base_url, ({} is not a valid value)".format(base_url))
            sys.exit(1)
        elif verify_ssl == "":
            print("You must provide a valid value for verify_ssl, ({} is not a valid value)".format(verify_ssl))
            sys.exit(1)
        else:
            # All values provided
            self.username,self.password,self.base_url,self.verify_ssl=username,password,base_url,verify_ssl

        data = {
            'grant_type': "password",
            'username': self.username,
            'password': self.password
        }
        # Create session object
        auth_session = requests.Session()
        # Perform post request to get access token
        r = auth_session.post("{}token".format(self.base_url),
                                                data=data,
                                                verify=self.verify_ssl
                                                )
        # Don't need to store this as instance variable, it's
        # implicitly stored with session
        try:
            access_token = r.json()['access_token']
            self.session_initialized = True
        except:
            print("Access token was not in response: response was {}".format(r.content))
            access_token = ""
        # Use session to always include "Authorization": "Bearer " + token as default header
        # Now this token is passed for all additional API calls inherently
        auth_session.headers.update({'Authorization': 'Bearer {}'.format(access_token)})
        self.auth_session = auth_session





    # Method to parse dictionary/JSON object from '{"key1":"val1","key2":"val2"}' data format
    # Input: string '{"key1":"val1","key2":"val2"}', never None
    # Returns: dictionary {"key1":"val1","key2":"val2"}
    def convert_data_to_requests_payload_format(self, data):
        return json.loads(data)

    def validate_data_keys(self,data,required_keys_list):
        for k in required_keys_list:
            if k not in data:
                return False
        return True
    def parseResponse(self,response,jsonContent):
        print(response)
        if jsonContent is not None :
            print(jsonContent)

    def route(self, endpoint,method,data):
        """
        Router method, direct endpoint request to proper method (e.g. subscribers, statuspage, updates, users ... )
        """

        # If data is passed in, convert it from string '{}' to dict {}
        data = self.convert_data_to_requests_payload_format(data) if data else None

        # Routers return Response and ONE of: [json.loads(response.content), None]
        if "account" in endpoint:
            r,j = self.account_router(endpoint,method,data)
        elif "components" in endpoint:
            r,j = self.components_router(endpoint,method,data)
        elif "search/incidents" in endpoint:
            r,j = self.search_incidents_router(endpoint,method,data)
        elif "incidents" in endpoint:
            r,j = self.incidents_router(endpoint,method,data)
        elif "metrics/custom" in endpoint:
            r,j = self.metricsCustom_router(endpoint,method,data)
        elif "statuspage" in endpoint:
            r,j = self.statuspage_router(endpoint,method,data)
        elif "subscribers" in endpoint:
            r,j = self.subscribers_router(endpoint,method,data)
        elif "updates" in endpoint:
            r,j = self.updates_router(endpoint,method,data)
        elif "users" in endpoint:
            r,j = self.users_router(endpoint,method,data)

        else:
            print("Invalid endpoint: {}".format(endpoint))
            sys.exit(1)

        self.parseResponse(r,j)

    def account_router(self,endpoint,method,data):
        """
        Router method for the /account endpoint
        Options from here are /forgotpassword,/resetpassword,/subscriptions
        """
        if "forgotpassword" in endpoint:
            # ONLY POST
            return self.account_forgotpassword(endpoint,method,data)
        elif "resetpassword" in endpoint:
            # ONLY POST
            return self.account_resetpassword(endpoint,method,data)
        elif "subscriptions" in endpoint:
            # GET OR POST
            return self.account_subscriptions_router(endpoint,method,data)
    @POST
    def account_forgotpassword(self,endpoint,method,data):
        """
        Handler for forgotpassword request, must be POST
        """
        # Ensure presence of required data fields
        required_data = ["emailaddress"]
        if self.validate_data_keys(data,required_data):
            r = self.auth_session.post("{}{}".format(self.base_url,endpoint),data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("POST request to {} requires data: {}".format(endpoint,','.join(required_data)))
            return None,None

    @POST
    def account_resetpassword(self,endpoint,method,data):
        """
        Handler for resetpassword request, must be POST
        """
        # Ensure presence of required data fields
        required_data = ["userid","token","password","confirmPassword"]
        if self.validate_data_keys(data,required_data):
            r = self.auth_session.post("{}{}".format(self.base_url,endpoint),data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("POST request to {} requires data: {}".format(endpoint,','.join(required_data)))
            return None,None


    def account_subscriptions_router(self,endpoint,method,data):
        """ Sub router for account_subscriptions; can be GET or POST """
        if m(method) == "get":
            return self.account_subscriptions_get("{}{}".format(self.base_url,endpoint),method,data)
        elif m(method) == "post":
            return self.account_subscriptions_post("{}{}".format(self.base_url,endpoint),method,data)
        else:
            print("{} is an invalid method for {}".format(method,endpoint))
            return None,None
    @GET
    def account_subscriptions_get(self, endpoint,method,data):
        """ Handler for GET account subcriptions request """
        print("Getting {}".format(endpoint))
        r = self.auth_session.get("{}{}".format(self.base_url,endpoint),verify=self.verify_ssl)
        return r, json.loads(r.content)

    @POST
    def account_subscriptions_post(self,endpoint,method,data):
        """ Handler for POST account subcriptions request """
        # Ensure presence of required data fields
        required_data = [
            "id","receiveMonthlySummary","smsSubscribeToDisruptionPosts",
            "smsSubscribeToInformationPosts","smsSubscribeToNormalPosts",
            "smsSubscribeToPerformancePosts","subscribeToDisruptionPosts",
            "subscribeToInformationPosts","subscribeToNormalPosts",
            "subscribeToPerformancePosts"
            ]

        if self.validate_data_keys(data,required_data):
            r = self.auth_session.post("{}{}".format(self.base_url,endpoint),data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("POST request to {} requires data: {}".format(endpoint,','.join(required_data)))
            return None,None


    def components_router(self,endpoint,method,data):
        """ Subrouter for the the /components endpoint """
        if m(method) == "get":
            return self.components_get("{}{}".format(self.base_url,endpoint),method,data)
        elif m(method) == "post":
            return self.components_create(endpoint,method,data)
        elif m(method) == "delete":
            return self.components_delete("{}{}".format(self.base_url,endpoint),method,data)
        elif m(method) == "put":
            return self.components_update(endpoint,method,data)
        else:
            print("{} is an invalid method for {}".format(method,endpoint))
            return None,None

    @GET
    def components_get(self,endpoint,method,data):
        """ Handler for components GET request; endpoint can be /components/<id> or /components """
        r = self.auth_session.get(endpoint,data=data,verify=self.verify_ssl)
        return r, json.loads(r.content)


    @POST
    def components_create(self,endpoint,method,data):
        """
        Handler for components POST request
        """
        # Ensure presence of required data fields
        required_data = ["name","description","priority","parentId","isHidden"]
        if self.validate_data_keys(data,required_data):
            r = self.auth_session.post(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("POST request to {} requires data: {}".format(endpoint,','.join(required_data)))
            return None,None

    @DELETE
    def components_delete(self,endpoint,method,data):
        """
        Handler for components DELETE request; endpoint must be /components/<id>
        """
        if "?id=" in endpoint:
            r = self.auth_session.delete(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("DELETE request to {} requires data: ?id=<id to delete> in URL".format(endpoint))
            return None,None

    @PUT
    def components_update(self,endpoint,method,data):
        """ Handler for components update request; endpoint must be /components?id=<id to update> """
        required_data = ["name","description","priority","parentId","isHidden"]
        if self.validate_data_keys(data,required_data) and "?id=" in endpoint:
            r = self.auth_session.put(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("DELETE request to {} requires data: {}".format(endpoint,','.join(required_data)))
            return None,None



    def incidents_router(self,endpoint,method,data):
        """ Subrouter for the the /incidents endpoint """
        if m(method) == "get":
            return self.incidents_get("{}{}".format(self.base_url,endpoint),method,data)
        elif m(method) == "post":
            return self.incidents_create(endpoint,method,data)
        elif m(method) == "delete":
            return self.incidents_delete("{}{}".format(self.base_url,endpoint),method,data)
        elif m(method) == "put":
            return self.incidents_update(endpoint,method,data)
        else:
            print("{} is an invalid method for {}".format(method,endpoint))
            return None,None

    @POST
    def incidents_create(self,endpoint,method,data):
        """
        Handler for incidents POST request
        """
        # Ensure presence of required data fields
        required_data = [
                    "dateToPost",
                    "incidentType",
                    "messageSubject",
                    "messageText",
                    "comScheduledMaintNightOfPosting",
                    "comScheduledMaintDaysBefore",
                    "comScheduledMaintHoursBefore",
                     "allowDisqus",
                    "active",
                    "happeningNow",
                    "treatAsDownTime",
                    "estimatedDuration",
                    "affectedComponents"
        ]
        if self.validate_data_keys(data,required_data):
            r = self.auth_session.post(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("POST request to {} requires data: {}".format(endpoint,','.join(required_data)))
            return None,None
    @DELETE
    def incidents_delete(self,endpoint,method,data):
        """
        Handler for incidents DELETE request; endpoint must be /incidents/<id>
        """
        if "?id=" in endpoint:
            r = self.auth_session.delete(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("DELETE request to {} requires data: ?id=<id to delete> in URL".format(endpoint))
            return None,None

    @PUT
    def incidents_update(self,endpoint,method,data):
        """ Handler for incidents update request; endpoint must be /incidents?id=<id to update> """
        required_data = [
                    "dateToPost",
                    "incidentType",
                    "messageSubject",
                    "messageText",
                    "comScheduledMaintNightOfPosting",
                    "comScheduledMaintDaysBefore",
                    "comScheduledMaintHoursBefore",
                     "allowDisqus",
                    "active",
                    "happeningNow",
                    "treatAsDownTime",
                    "estimatedDuration",
                    "affectedComponents"
        ]
        if self.validate_data_keys(data,required_data) and "?id=" in endpoint:
            r = self.auth_session.put(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("PUT request to {} requires ?id=<id to update> at end of URL and data payload {}".format(endpoint,','.join(required_data)))
            return None,None
    @GET
    def incidents_get(self,endpoint,method,data):
        """ Handler for incidents GET request; endpoint can be:
         /incidents?id=<id>
         /inicdents/?start=<startdate>&end=<enddate>
         /incidents/incidenttypes
          """
        # Doesn't require parameters, so just execute request
        if "incidenttypes" in endpoint:
            r = self.auth_session.get(endpoint,verify=self.verify_ssl)
            return r, json.loads(r.content)
        elif "?id=" in endpoint:
            r = self.auth_session.get(endpoint,verify=self.verify_ssl)
            return r, json.loads(r.content)
        elif "?start=" in endpoint and "end=" in endpoint:
            r = self.auth_session.get(endpoint,verify=self.verify_ssl)
            return r, json.loads(r.content)
        else:
            print("Cannot perform GET request on endpoint {}".format(endpoint))
            return None,None


    @POST
    def metricsCustom_router(self, endpoint,method,data):
        """ Handler for the metrics/custom POST request """
        required_data = ["id","value","timestamp"]
        if self.validate_data_keys(data,required_data):
            r = self.auth_session.post("{}{}".format(self.base_url,endpoint),data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("POST request to {} requires data: {}".format(endpoint,','.join(required_data)))
            return None,None
    @GET
    def search_incidents_router(self,endpoint,method,data):
        """ Router for search incidents GET request; must include at least one of any of the following optional params:
        componentId		optional		Number		reduce the query to a specific component
        minDate			optional		Date		reduce the query to dates greater than or equal to this parameter
        maxDate			optional		Date		reduce the query to dates less than or equal to this parameter
        includeChildren	optional		Boolean		when given a componentId, include that component's children as part of the result.
        """
        r = self.auth_session.get("{}{}".format(self.base_url,endpoint),verify=self.verify_ssl)
        return r, json.loads(r.content)



    def statuspage_router(self,endpoint,method,data):
        """ Router for /statuspage requests """
        if "addhit" in endpoint:
            return self.statuspage_addhit("{}{}".format(self.base_url,endpoint),method,data)
        elif "css" in endpoint:
            return self.statuspage_css("{}{}".format(self.base_url,endpoint),method,data)
        elif "calendarevents" in endpoint:
            return self.statuspage_calendarevents("{}{}".format(self.base_url,endpoint),method,data)
        elif "dashboardposts" in endpoint:
            return self.statuspage_dashboardposts("{}{}".format(self.base_url,endpoint),method,data)
        elif "dashboardgrid" in endpoint:
            return self.statuspage_dashboardgrid("{}{}".format(self.base_url,endpoint),method,data)
        elif "metrics" in endpoint:
            return self.statuspage_metrics("{}{}".format(self.base_url,endpoint),method,data)
        elif "settings" in endpoint:
            return self.statuspage_settings("{}{}".format(self.base_url,endpoint),method,data)
        elif endpoint.endswith('statuspage') or endpoint.endswith('statuspage/'):
            # Valid get request, must be GET though. No data/payload.
            r = self.auth_session.get("{}{}".format(self.base_url,endpoint),verify=self.verify_ssl)
            return r, json.loads(r.content)
        else:
            print("Invalid endpoint given: {}".format(endpoint))
            return None,None

    @POST
    def statuspage_addhit(self,endpoint,method,data):
        """ Handler for POST /statuspage/addhit request """
        # Rare: post request that does not require data; hits an endpoint, increments a counter on their end.
        r = self.auth_session.post(endpoint,data=data,verify=self.verify_ssl)
        return r, r.content
    @GET
    def statuspage_css(self,endpoint,method,data):
        """ Handler for GET /statuspage/css request """
        r = self.auth_session.get(endpoint,data=data,verify=self.verify_ssl)
        return r, r.content # Not json; is a CSS string e.g. "body { background: white }"

    @GET
    def statuspage_calendarevents(self, endpoint,method,data):
        """ Handler for GET /statuspage/calendarevents
        Requires start and end date
        """
        if "?start=" in endpoint and "end=" in endpoint:
            r = self.auth_session.get(endpoint,data=data,verify=self.verify_ssl)
            return r, json.loads(r.content)
        else:
            print("GET request to {} requires data: ?start=<start date>&end=<end date> in URL".format(endpoint))
            return None,None
    @GET
    def statuspage_dashboardposts(self, endpoint,method,data):
        """ Handler for GET /statuspage/dashboardposts
        Requires date to receive posts for
         """
        if "?date=" in endpoint:
            r = self.auth_session.get(endpoint,data=data,verify=self.verify_ssl)
            return r, json.loads(r.content)
        else:
            print("GET request to {} requires data: ?date=<date to receive posts> in URL".format(endpoint))
            return None,None
    @GET
    def statuspage_dashboardgrid(self, endpoint,method,data):
        """ Handler for GET /statuspage/dashboardgrid
        Requires offset (number of days offset from current date)
        """
        if "?offset=" in endpoint:
            r = self.auth_session.get(endpoint,data=data,verify=self.verify_ssl)
            return r, json.loads(r.content)
        else:
            print("GET request to {} requires data: ?offset=<number of days offset from current date> in URL".format(endpoint))
            return None,None

    @GET
    def statuspage_metrics(self, endpoint,method,data):
        """ Handler for GET /statuspage/metrics
        Requires:
        type: pingdom, newrelic or custom
        period: day, week or month
        metricId: id of metric to receive data for
        """
        if "type=" in endpoint and "period=" in endpoint and "metricId=" in endpoint:
            r = self.auth_session.get(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("GET request to {} requires data: ?type=<pingdom, newrelic or custom>&period=<Day,Week,Month>&metricId=<id of metric to get data for> in URL".format(endpoint))
            return None,None
    @GET
    def statuspage_settings(self, endpoint,method,data):
        """ Handler for GET /statuspage/settings """
        r = self.auth_session.get(endpoint,data=data,verify=self.verify_ssl)
        return r, json.loads(r.content)



    def subscribers_router(self,endpoint,method,data=None):
        """
        Router method for the subscribers endpoint
        Options from here are GET, POST, DELETE
        """
        if m(method) == "delete":
            return self.subscribers_delete("{}{}".format(self.base_url,endpoint),method,data)
        elif m(method) == "post":
            return self.subscribers_invite("{}{}".format(self.base_url,endpoint),method,data)
        elif m(method) == "get":
            return self.subscribers_list("{}{}".format(self.base_url,endpoint),method,data)
        else:
            print("{} is an invalid method for {}".format(method,endpoint))
            return None,None

    @DELETE
    def subscribers_delete(self, endpoint,method,data):
        """
        Handler for subscriber DELETE request; endpoint must be /components/<id to delete>
        """
        if "?id=" in endpoint:
            r = self.auth_session.delete(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("DELETE request to {} requires data: ?id=<id to delete> in URL".format(endpoint))
            return None,None


    @POST
    def subscribers_invite(self, endpoint,method,data):
        """
        Handler for the POST subscriber invite request, requires :
        "emailAddress": <email of invitee>
        "createAccount": <whether or not to go ahead and create an account for them>
        "sendPassword": <whether or not to send password for that account to them>
        "components": [ < list of ids of components to subscribe them to by default > ]
         """
        required_data = ["emailAddress","createAccount","sendPassword","components"]
        if self.validate_data_keys(data,required_data):
            r = self.auth_session.post(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("POST request to {} requires data: {}".format(endpoint,','.join(required_data)))
            return None,None

    @GET
    def subscribers_list(self, endpoint,method,data):
        """ Handler for GET subscribers List request, optional params; can be in URL or data
        componentId		Number		filter by component
        currentPage		Number		page of results to return (defaults to 1)
        searchText		String		search by email address or full name
        """
        r = self.auth_session.get(endpoint,data=data,verify=self.verify_ssl)
        return r, json.loads(r.content)


    def updates_router(self,endpoint,method,data):
        """
        Router for /updates endpoint ; can create, delete or get details about update
        """
        if m(method) == "post":
            return self.updates_create("{}{}".format(self.base_url,endpoint),method,data)
        if m(method) == "delete":
            return self.updates_delete("{}{}".format(self.base_url,endpoint),method,data)
        if m(method) == "get":
            return self.updates_get("{}{}".format(self.base_url,endpoint),method,data)

    @POST
    def updates_create(self,endpoint,method,data):
        """ Handler for POST /updates request ; requires data, example :
        {
            "postId": 27638,
            "datePosted": "12/12/2014",
            "messageText": "update",
            "postType": 2
        }
        """
        required_data = ["postId","datePosted","messageText","postType"]
        if self.validate_data_keys(data,required_data):
            r = self.auth_session.post(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("POST request to {} requires data: {}".format(endpoint,','.join(required_data)))
            return None,None

    @DELETE
    def updates_delete(self,endpoint,method,data):
        """
        Handler for /updates DELETE request; endpoint must be /updates?=<id to delete>
        """
        if "?id=" in endpoint:
            r = self.auth_session.delete(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("DELETE request to {} requires data: ?id=<id to delete> in URL".format(endpoint))
            return None,None

    @GET
    def updates_get(self,endpoint,method,data):
        """
        Handler for /updates GET request; endpoint must be /updates?=<id to get details for>
        """
        if "?id=" in endpoint:
            r = self.auth_session.get(endpoint,data=data,verify=self.verify_ssl)
            return r, json.loads(r.content)
        else:
            print("GET request to {} requires ?id=<id to get details for> at end of URL".format(endpoint))
            return None,None


    def users_router(self,endpoint,method,data):
        """ Router for /users request ; can be Delete, Get, Put or Post"""
        if m(method) == "delete":
            return self.users_delete("{}{}".format(self.base_url,endpoint),method,data)
        if m(method) == "get":
            return self.users_get("{}{}".format(self.base_url,endpoint),method,data)
        if m(method) == "post":
            return self.users_post("{}{}".format(self.base_url,endpoint),method,data)
        if m(method) == "put":
            return self.users_put("{}{}".format(self.base_url,endpoint),method,data)
        else:
            print("{} is an invalid method for endpoint {}; only accepts delete,get,put,post".format(method,endpoint))
            return None,None

    @DELETE
    def users_delete(self,endpoint,method,data):
        """ Handler for /users DELETE request , requires id as param """
        if "?id=" in endpoint:
            r = self.auth_session.delete(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("DELETE request to {} requires data: ?id=<id to delete> in URL".format(endpoint))
            return None,None
    @GET
    def users_get(self,endpoint,method,data):
        """ Handler for /users GET request; optional /:<id of user> """
        r = self.auth_session.get(endpoint,data=data,verify=self.verify_ssl)
        return r, json.loads(r.content)

    @PUT
    def users_put(self,endpoint,method,data):
        """ Handler for /users PUT request, data required:
        {
        "userName": "bill@example.com",   // must be a valid email address
        "fullName": "Bill Smith",         // optional
        "adminAccess": "Full"             // Full, PostOnly, None
        }
        plus ?id=<id of user to update> at end of url
        """

        required_data = ["userName","fullName","adminAccess"]
        if self.validate_data_keys(data,required_data) and "?id=" in endpoint:
            r = self.auth_session.put(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("PUT request to {} requires ?id=<id of user to update> at end of URL and " + \
                        "data payload: {}".format(endpoint,','.join(required_data)))
            return None,None
    @POST
    def users_post(self,endpoint,method,data):
        """ Handler for /users POST request, data required:
        {
        "userName": "bill@example.com",   // must be a valid email address
        "fullName": "Bill Smith",         // optional
        "adminAccess": "Full"             // Full, PostOnly, None
        }
        """
        required_data = ["userName","fullName","adminAccess"]
        if self.validate_data_keys(data,required_data):
            r = self.auth_session.post(endpoint,data=data,verify=self.verify_ssl)
            return r, r.content
        else:
            print("POST request to {} requires data: {}".format(endpoint,','.join(required_data)))
            return None,None


