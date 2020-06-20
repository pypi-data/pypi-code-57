import time
import requests

from . import exceptions

class SmsArea:
    """
    Официальная документация: http://sms-area.org/api.txt
    Репозитортй на github.com: https://github.com/daveusa31/sms_area_api
    
    Доступные методы:
        get_balance
        get_number
        set_status
        get_status
    """
    __API_URL = "http://sms-area.org/stubs/handler_api.php"

    def __init__(self, api_key):
        """
        Параметры:
            api_key : str
                Ваш api ключ со страницы http://sms-area.org/settings.php
        """
        self.__api_key = api_key

        self.__session = requests.Session()

    def get_balance(self):
        """
        Баланс аккаунта
        Возрат:
            balane : float
        """
        params = {
            "action": "getBalance",
        }

        balance = self.__request(params).split(":")[1]
        return float(balance)

    def get_number(self, service, count=1, country="or"):
        """
        Получение номера

        Параметры:
            service : str
                Нужный сервис
            count : Optional[int]
                Планируемое количество смс на получаемый номер
                По умолчанию 1
            country : Optional[str]
                По умолчанию or
                Нужная страна

        Возрат:
            dict: 

        """
        params = {
            "action": "getNumber",
            "country": country,
            "service": service,
            "count": count,
        }
        response_array = self.__request(params).split(":")[1:]
        
        order_id, phone = response_array

        response = {
            "order_id": int(order_id),
            "phone": int(phone),
        }

        return response

    def set_status(self, order_id, status):
        params = {
            "action": "setStatus",
            "id": int(order_id),
            "status": int(status),
        }
        return self.__request(params)


    def get_status(self, order_id):
        params = {
            "action": getStatus,
            "id": order_id,
        }
        return self.__request(params)




    def __request(self, params):
        params["api_key"] = self.__api_key
        response = requests.post(self.__API_URL, params).text


  
        if "BAD_KEY" == response:
            raise exceptions.BadKey("Invalid api_key")

        elif "NO_MEANS" == response:
            raise exceptions.NoMeans("Not enough money on the balance")

        elif "NO_NUMBER" == response:
            raise exceptions.NoNumber("Not need number")

        elif "NO_ACTIVATORS_RATE" == response:
            error_text = "The rate of activators is higher than yours"
            raise exceptions.NoActivatorsRate(error_text)


        return response