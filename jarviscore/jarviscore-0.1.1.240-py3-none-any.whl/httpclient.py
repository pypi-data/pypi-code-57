from requests import get, patch, put, post
from .settings import Settings
from .log import Log
from .model import Model
from .errors import DBConnectionUndefined, HTTPDriverNotConfigured
from urllib import parse

class WebResponse():
    def __init__(self, data:dict):
        self.status = data["status"]
        self.message = data["message"]
        self.code = data["code"]
        self.text = data["text"]
        self.json = data["json"]
        self.headers = data["headers"]

    def __repr__(self):
        return f"[{self.status}]({self.message}): {self.text}"


class HTTPClient():

    def __init__(self, owner:str, use_model=False, twitch_oauth=None):
        self.log = Log("Web Handler", f"Web Handler: {owner}")
        self.useModel = False
        if use_model:
            self.model = Model()
            self.useModel = True
        self.twitchToken = twitch_oauth

    def GetFromTwitch(self, url: str) -> WebResponse:
        headers = self.__get_twitch_headers(url)
        return self.Get(url, headers=headers)

    def GetFromDiscord(self, url: str) -> WebResponse:        
        headers = self.__get_discord_headers()
        return self.Get(url, headers=headers)

    def PutToTwitch(self, url: str, body: dict) -> WebResponse:
        headers = self.__get_twitch_headers(url)
        return self.Put(url, body=body, headers=headers)
    
    def PutJSONToTwitch(self, url: str, body: dict) -> WebResponse:
        headers = self.__get_twitch_headers(url)
        return self.PutJSON(url, body=body, headers=headers)

    def PostFormToTwitch(self, url:str,  body: dict) -> WebResponse:
        headers = self.__get_twitch_headers(url)
        return self.PostForm(url=url, body=body, headers=headers)

    def PostFormToDiscord(self, url:str,  body: dict) -> WebResponse:
        headers = self.__get_discord_headers()
        return self.PostForm(url=url, body=body, headers=headers)

    def PostJSONToTwitch(self, url:str,  body: dict) -> WebResponse:
        headers = self.__get_twitch_headers(url)
        return self.PostJSON(url=url, body=body, headers=headers)

    def PostJSONToDiscord(self, url:str,  body: dict) -> WebResponse:
        headers = self.__get_discord_headers()
        return self.PostJSON(url=url, body=body, headers=headers)



    def Get(self, url: str, headers: dict = None) -> dict:
        """Get request"""           
        self.log.debug(f"Sending new GET request to '{url}'.\nHeaders: \n{headers}")
        try:
            response = get(url=url, headers=headers)
        except Exception as ex:
            return self.__exception_response(str(ex))
        rt = self.__process_response(response)
        self.log.debug("returning: \n{}".format(rt))
        return rt

    def Put(self, url: str, body: dict, headers: dict = None):
        """Put request"""           
        self.log.debug(f"Sending new PUT request to '{url}'.\nHeaders: \n{headers}\nBody:\n{body}")
        try:
            response = put(url=url, data=body, headers=headers)
        except Exception as ex:
            return self.__exception_response(str(ex))
        rt = self.__process_response(response)
        self.log.debug("returning: \n{}".format(rt))
        return rt
    
    def PutJSON(self, url: str, body: dict, headers: dict = None):
        """Put request"""           
        self.log.debug(f"Sending new PUT request to '{url}'.\nHeaders: \n{headers}\nBody:\n{body}")
        try:
            response = put(url=url, json=body, headers=headers)
        except Exception as ex:
            return self.__exception_response(str(ex))
        rt = self.__process_response(response)
        self.log.debug("returning: \n{}".format(rt))
        return rt


    
    def PostForm(self, url:str,  body: dict, headers: dict = None):
        if headers is None:
            setting = Settings()
            headers = {
                "Client-ID": setting.get_setting("tokens.twitch.user"), 
                "content-type": 'application/x-www-form-urlencoded', 
            }
        self.log.debug(f"Sending new POST request to '{url}'.\nHeaders: \n{headers}\nBody:\n{body}")
        try:
            response = post(url=url, headers=headers, data=body)
        except Exception as ex:
            return self.__exception_response(str(ex))
        rt = self.__process_response(response)
        self.log.debug("returning: \n{}".format(rt))
        return rt
    
    def PostJSON(self, url:str,  body: dict, headers: dict = None):
        if headers is None:
            setting = Settings()
            headers = {
                "Client-ID": setting.get_setting("tokens.twitch.user"), 
                "content-type": 'application/json', 
            }
        self.log.debug(f"Sending new POST request with JSON body to '{url}'.\nHeaders: \n{headers}\nBody:\n{body}")
        response = post(url=url, headers=headers, json=body)
        try:
            rt = self.__process_response(response)
        except Exception as ex:
            return self.__exception_response(str(ex))
        self.log.debug("returning: \n{}".format(rt))
        return rt
    
    def __exception_response(self, message):
        self.log.warn("An exception occrred when attempting to contact the server. Exception: " + message)
        return WebResponse ({
            "status": "error",
            "message": "an exception occurred when attempting to contact server.",
            "code": 600,
            "text": message,
            "json": {"error": message},
            "headers": None
        })


    def __process_response(self, response):
        if response.status_code == 200:
            self.log.debug("Response: 200 | OK \n Headers:\n{}\n\nContent:\n{}".format(response.headers, response.text))
            return WebResponse ({
                "status": "ok",
                "message": "response ok",
                "code": response.status_code,
                "text": response.text,
                "json": response.json(),
                "headers": response.headers
            })
        elif response.status_code == 201:
            self.log.debug("Response: 201 | OK \n Headers:\n{}\n\nContent:\n{}".format(response.headers, response.text))
            return WebResponse ({
                "status": "ok",
                "message": "no data returned",
                "code": response.status_code,
                "text": "No Data",
                "json": {"No Data"},
                "headers": response.headers
            })
        elif response.status_code == 202:
            self.log.debug("Response: 202 | Accepted \n Headers:\n{}\n\nContent:\n{}".format(response.headers, response.text))
            return WebResponse ({
                "status": "ok",
                "message": "accepted",
                "code": response.status_code,
                "text": "No Data",
                "json": {"No Data"},
                "headers": response.headers
            })
        elif response.status_code == 204:
            self.log.debug("Response: 204 | No Content \n Headers:\n{}\n\nContent:\n{}".format(response.headers, response.text))
            return WebResponse ({
                "status": "ok",
                "message": "no content",
                "code": response.status_code,
                "text": "No Data",
                "json": {"No Data"},
                "headers": response.headers
            })
        elif response.status_code == 400:
            self.log.info("Response: 400 | Bad Request \n Headers:\n{}\n\nContent:\n{}".format(response.headers, response.text))
            return WebResponse ({
                "status": "error",
                "message": "bad request",
                "code": response.status_code,
                "text": response.text,
                "json": response.json(),
                "headers": response.headers
            })
        elif response.status_code == 401:
            self.log.info("Response: 401 | Unauthorised Request \n Headers:\n{}\n\nContent:\n{}".format(response.headers, response.text))
            return WebResponse ({
                "status": "error",
                "message": "unauthorised request",
                "code": response.status_code,
                "text": response.text,
                "json": response.json(),
                "headers": response.headers
            })
        elif response.status_code == 404:
            self.log.info("Response: 404 | Resource not found \n Headers:\n{}\n\nContent:\n{}".format(response.headers, response.text))
            return WebResponse ({
                "status": "error",
                "message": "resource not found",
                "code": response.status_code,
                "text": response.text,
                "json": response.json(),
                "headers": response.headers
            })
        else:
            self.log.error("Response: {} | \nHeaders: {} \nError Response\n{}".format(response.status_code, response.headers, response.text))
            return WebResponse ({               
                "status": "error",
                "message": "server returned an error",
                "code": response.status_code,
                "text": response.text,
                "json": response.json(),
                "headers": response.headers
            })

    def __get_twitch_headers(self, url: str) -> dict:
        setting = Settings()
        token = ""

        if self.twitchToken is None and not self.useModel:
            raise HTTPDriverNotConfigured("Values provided for DB connection / Twitch OAuth are invalid.\nYou must provide either:\n - Values for the Databse with 'db_user' and 'db_pass'\n - An OAuth token for the Twitch API")

        elif self.twitchToken is not None:
            token = self.twitchToken
        
        else:
            jOAUTH = self.model.fetchOne("select AccessToken from Tokens where TokenType = 'JarvisAppToken'")
            token = jOAUTH[0]

        if "kraken" in url:
            headers = {
                "Client-ID" : setting.get_setting("tokens.twitch.user"),
                "Authorization": "OAuth " + token,
                "Accept": "application/vnd.twitchtv.v5+json"
            }
        else:
            headers = {
                "Client-ID" : setting.get_setting("tokens.twitch.user"),
                "Authorization": "Bearer " + token
            }

        return headers

    
    def __get_discord_headers(self) -> dict:
        setting = Settings()
        headers = {
            "Client-ID": "{}".format(setting.get_setting("integration.discord.client")),
            "User-Agent": setting.get_setting("integration.discord.agent"),
            "Authorization": "Bot {}".format(setting.get_setting("integration.discord.key"))
        }
        return headers