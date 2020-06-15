import logging
import requests
from time import sleep


logger = logging.getLogger(__name__)

REQUESTS_TIMEOUT = (5.0, 30.0)
MAX_RETRIES = 3
BACKOFF_FACTOR = 0.3

HTTP_BAD_GATEWAY = 502
HTTP_SERVICE_UNAVAILABLE = 503
HTTP_GATEWAY_TIMEOUT = 504


class WebhookResponse:
    """response from a Discord Webhook"""

    def __init__(
        self, headers: dict, status_code: int, content: dict = None
    ) -> None:
        self._headers = dict(headers)
        self._status_code = int(status_code)
        self._content = dict(content) if content else None

    @property
    def headers(self) -> dict:
        """response headers"""
        return self._headers 

    @property
    def status_code(self) -> int:
        """HTTP status code of the response"""
        return self._status_code 

    @property
    def content(self) -> dict:
        """content of the response, e.g. send report
        
        will be empty if not waited for response from Discord
        """
        return self._content 

    @property
    def status_ok(self) -> bool:
        """whether the response was ok based on its HTTP status"""
        return self._status_code >= 200 and self._status_code <= 299


class Webhook:
    """A Discord Webhook"""

    MAX_CHARACTERS = 2000

    def __init__(
        self, url: str, username: str = None, avatar_url: str = None
    ) -> None:
        """Initialize a Webhook object
        
        Parameters
        
        - url: Discord webhook url
        - username: Override default user name of the webhook
        - avatar_url: Override default avatar icon of the webhook with image URL        
        """
        if not url:
            raise ValueError('url must be specified')

        self._url = str(url)
        self._username = str(username) if username else None
        self._avatar_url = str(avatar_url) if avatar_url else None
    
    @property
    def url(self) -> str:
        return self._url
    
    @property
    def username(self) -> str:
        return self._username

    @property
    def avatar_url(self) -> str:
        return self._avatar_url
        
    def execute(
        self, 
        content: str = None,            
        embeds: list = None,
        tts: bool = None,
        username: str = None, 
        avatar_url: str = None,
        wait_for_response: bool = False
    ) -> WebhookResponse:
        """Posts a message to this webhook
        
        Parameters
        
        - content: Text of this message
            
        - embeds:List of Embed objects to be attached to this message
            
        - tts: Whether or not the message will use text-to-speech
            
        - username: Overrides default user name of the webhook
        
        - avatar_url: Override default avatar icon of the webhook with image URL
        
        - wait_for_response: Whether or not to wait for a send report 
        from Discord (defaults to ``False``). 
        
        Exceptions
                
        - ValueError: on invalid input

        - ConnectionError: on network issues
        
        - Timeout: if timeouts are exceeded

        - TooManyRedirects: if configured redirect limit is exceeded
        
        Returns
               
        - response from webhook as WebhookResponse object
         
        """
        if not content and not embeds:
            raise ValueError('need content or embeds')
                
        payload = dict()        
        self._set_content(payload, content)
        self._set_embeds(payload, embeds)
        self._set_username(payload, username)
        self._set_avatar_url(payload, avatar_url)
        self._set_tts(payload, tts)
                        
        retry_count = 0
        for retry_count in range(MAX_RETRIES + 1):            
            logger.debug(
                'Sending request to \'%s\' with payload: %s', self._url, payload
            )
            r = requests.post(
                url=self._url,
                params={'wait': bool(wait_for_response)},
                json=payload,
                timeout=REQUESTS_TIMEOUT
            )
            if not r.ok:
                logger.warning('HTTP status code: %s', r.status_code)
            else:
                logger.debug('HTTP status code: %s', r.status_code)
            
            logger.debug('Response headers from Discord: %s', r.headers)
            logger.debug('Response from Discord: %s', r.content)
        
            if (
                r.status_code in [
                    HTTP_BAD_GATEWAY, HTTP_GATEWAY_TIMEOUT, HTTP_SERVICE_UNAVAILABLE
                ]
            ):
                retry_count += 1
                if retry_count <= MAX_RETRIES:
                    logger.warning('Retry %d / %d', retry_count, MAX_RETRIES)
                    if retry_count > 1:
                        wait_secs = BACKOFF_FACTOR * (2 ** (retry_count - 1))
                        sleep(wait_secs)
            else:
                break
            
        try:
            content_returned = r.json()
        except ValueError:
            content_returned = None

        response = WebhookResponse(
            headers=r.headers,
            status_code=r.status_code,
            content=content_returned
        )        
        return response

    def _set_content(self, payload: dict, content: str) -> None:
        if content:
            content = str(content)
            if len(content) > self.MAX_CHARACTERS:
                raise ValueError(
                    'content exceeds {}'.format(self.MAX_CHARACTERS)
                )
            payload['content'] = content

    def _set_embeds(self, payload: dict, embeds: list) -> None:
        if embeds:
            if not isinstance(embeds, list):
                raise TypeError('embeds must be of type list')
            
            for embed in embeds:
                if type(embed).__name__ != 'Embed':
                    raise TypeError('embeds elements must be of type Embed')
            
            payload['embeds'] = [x.to_dict() for x in embeds]

    def _set_username(self, payload: dict, username: str) -> None:
        if not username and self._username:
            username = self._username

        if username:
            payload['username'] = str(username)

    def _set_avatar_url(self, payload: dict, avatar_url: str) -> None:
        if not avatar_url and self._avatar_url:
            avatar_url = self._avatar_url

        if avatar_url:
            payload['avatar_url'] = str(avatar_url)

    def _set_tts(self, payload: dict, tts: bool) -> None:
        if tts:
            if not isinstance(tts, bool):
                raise TypeError('tts must be of type bool')

            payload['tts'] = tts
