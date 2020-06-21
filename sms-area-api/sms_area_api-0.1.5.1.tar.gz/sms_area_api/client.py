import requests

from . import exceptions


class SmsArea:
    """
    Официальная документация: http://sms-area.org/api/ru/documentation.html
    Репозитортй на github.com: https://github.com/daveusa31/sms_area_api
    
    Доступные методы:
        balance
        get_activation_list
        get_activation_status
    """

    __API_URL = "http://sms-area.org/api/handler.php"

    def __init__(self, api_key):
        """
        Параметры:
            api_key : str
                Ваш api ключ со страницы http://sms-area.org/settings.php
        """
        self.api_key = api_key

    def balance(self):
        """
        Баланс аккаунта
        Возрат:
            balane : float
        """
        params = {
            "method": "getBalance",
        }

        balance = self.__request(params)["balance"]
        return float(balance)

    def get_activation_list(self):
        """
        Метод предназначен для получения списка текущих 
        активаций (со статусами от 0 до 5). 
        Параметр "category" позволяет указать какие активации 
        нужно получить: заказанные с данного аккаунта (исходящие) 
        или заказанные у данного аккаунта (входящие).
        """
        params = {
            "method": "getActivationList",
        }
        return self.__request(params)

    def get_activation_status(self, id_activation: int):
        params = {
            "method": "getActivationStatus",
            "id_activation": int(id_activation),
        }
        return self.__request(params)

    def set_activation_status(self, id_activation: int, status: int):
        params = {
            "method": "getActivationStatus",
            "id_activation": int(id_activation),
            "status": int(status),
        }
        return self.__request(params)

    def get_activation_summary(self):
        """
        Этот метод заключается в том, 
        чтобы получить количество доступных номеров, 
        разделенных по стране, сервису и цене.
        """
        params = {
            "method": "getActivationSummary",
        }
        return self.__request(params)["summary"]

    def get_activation_rates(self):
        """
        Метод предназначен для получения размера ставок 
        установленных на аккаунте.
        """
        params = {
            "method": "getActivationRates",
        }
        return self.__request(params)

    def set_activation_rates(self, rate_list: dict):
        params = {
            "method": "setActivationRates ",
            "rate_list": rate_list,
        }
        return self.__request(params)

    def load_activation_history(
        self, category: str, limit: int, id_last: int, pattern: str
    ):
        params = {
            "method": "loadActivationHistory",
            "category": int(pattern),
            "limit": int(limit),
            "id_last": int(id_last),
            "pattern": pattern,
        }
        return self.__request(params)

    def get_number(self, service, pattern="or"):
        """
        Метод предназначен для получения номера и создания активации на него.
        Параметр "pattern" позволяет найти номер с помощью 
        регулярного выражения, 
        что дает большую свободу: можно выбрать номер определенной страны, 
        оператора и даже определенного региона. 
        Кроме того, это позволяет получить какой-либо конкретный номер, если, 
        например, требуется дополнительная SMS на уже активированный номер.
        """
        in_country_max_numbers = {
            "name": "",
            "amount": 0,
        }

        if "or" == pattern:
            response = self.get_activation_summary()

            for country, services in response.items():
                price_and_aviable = services[service]
                price = list(price_and_aviable)[0]
                aviable_numbers = int(price_and_aviable[price])
                if in_country_max_numbers["amount"] < aviable_numbers:
                    in_country_max_numbers["name"] = country
        else:
            in_country_max_numbers["name"] = pattern

        params = {
            "method": "runActivation",
            "service": service,
            "pattern": in_country_max_numbers["name"],
        }
        return self.__request(params)

    def aviable_numbers(self, service: str, country="or"):
        response = self.get_activation_summary()

        if "or" == country:
            aviable_numbers = 0

            for _country, services in response.items():
                price_and_aviable = services[service]
                price = list(price_and_aviable)[0]
                aviable_numbers += int(price_and_aviable[price])

        else:
            price_and_aviable = response[country][service]
            price = list(price_and_aviable)[0]
            aviable_numbers = int(price_and_aviable[price])

        return aviable_numbers

    def aviable_services(self, country="or"):
        """
        Список доступных сервисов
        """
        aviable_services = []

        response = self.get_activation_summary()
        if "or" == country:
            for _country, services in response.items():
                for service in services:
                    aviable_services.append(service)
        else:
            for service in response[country]:
                aviable_services.append(service)

        return aviable_services

    def service_price(self, service: str, country="or"):
        price = 0
        response = self.get_activation_summary()

        if "or" == country:
            aviable_numbers = 0

            for _country, services in response.items():
                price_and_aviable = services[service]
                now_price = float(list(price_and_aviable)[0])
                if price < now_price:
                    price = now_price

        else:
            price_and_aviable = response[country][service]
            price = float(list(price_and_aviable)[0])

        return price

    def __request(self, params):
        params["key"] = self.api_key
        response = requests.post(self.__API_URL, params).json()

        if 0 > int(response["response"]):
            raise exceptions.ApiError(response["description"])

        if 0 < len(response["data"]):
            response = response["data"]
        else:
            response = int(response["response"])

        return response
