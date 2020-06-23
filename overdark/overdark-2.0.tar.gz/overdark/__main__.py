import json
import urllib.parse
import requests


class Request(object):
    """
    Class request of overdark api
    docs: https://overdarkgame.com/langs/it/api/#/documentation
    author: t.me/tappo03
    """

    def __init__(self, lang: str, token: str, array: bool = False):
        """
        :param lang: string language of api result
        :param token: string your api Token get by from t.me/OverDarkAPI_bot, if you not have, register to bot
        :param array: bool choice of object return or array return
        """
        self._token = token
        self._array = array
        self._lang = lang

    def get_profile(self, tag: str) -> json:
        """
        Accedi alle informazioni del profilo del giocatore
        :param tag: string tag of Player
        :return: json information of user
        """

        request = requests.get(
            'https://api.overdarkgame.com/get_profile.php?tag={0}&token={1}&lang={2}'.format(urllib.parse.quote(tag),
                                                                                             urllib.parse.quote(self._token),
                                                                                             urllib.parse.quote(self._lang)))
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            raise Exception('Error request status_code = {}'.format(request.status_code))

    def get_clan(self, clan_id: str) -> json:
        """
        Accedi alle informazioni del clan
        :param clan_id: string tag of clan (id)
        :return: json info of clan
        """
        request = requests.get(
            'https://api.overdarkgame.com/get_clan.php?tag={0}&token={1}&lang={2}'.format(urllib.parse.quote(clan_id),
                                                                                          urllib.parse.quote(self._token),
                                                                                          urllib.parse.quote(self._lang)))
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            raise Exception('Error request status_code = {}'.format(request.status_code))

    def get_char_info(self) -> json:
        """
        Accedi alle informazioni dei personaggi
        :return: json
        """
        request = requests.get(
            'https://api.overdarkgame.com/get_char_info.php?token={0}&lang={1}'.format(urllib.parse.quote(self._token),
                                                                                       urllib.parse.quote(self._lang)))
        if request.status_code == 200:
            return json.loads(request.content)
        else:
            raise Exception('Error request status_code = {}'.format(request.status_code))

    def get_classification(self, type_classification: str) -> json:
        """
        Accedi alle informazioni sulla classifica dei giocatori
        :param type_classification: string type of classification you want, you can select from: overworld or darkworld
        :return: json return of classification
        """
        request = requests.get(
            'https://api.overdarkgame.com/get_char_info.php?type={0}&token={1}&lang={2}'.format(urllib.parse.quote(type_classification),
                                                                                                urllib.parse.quote(self._token),
                                                                                                urllib.parse.quote(self._lang)))

        if request.status_code == 200:
            return json.loads(request.content)
        else:
            raise Exception('Error request status_code = {}'.format(request.status_code))

    def get_player_image(self, image_id: int, background: bool = True) -> str:
        """
        Accedi alla foto profilo del giocatore
        :param image_id: int Image id of player, you found this on get_profile
        :param background: bool type of backgroun (If void this set automatically default image type (with_background) for set image type, you can select from: with_background or without_background)
        :return: str return of image (return link)
        """
        if background:
            image_type = 'with_background'
        else:
            image_type = 'without_background'

        return 'https://api.overdarkgame.com/get_player_image.php?type={0}&token={1}&id={2}'.format(urllib.parse.quote(image_type),
                                                                                                    urllib.parse.quote(self._token),
                                                                                                    urllib.parse.quote(str(image_id)))
