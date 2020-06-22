import requests

from . import exceptions

class FiveSms:
    """
    Официальная документация: https://5sim.net/docs/api_ru.txt?6a1b9db50e
    Репозитортй на github.com: https://github.com/daveusa31/fivesms-api
    
    Доступные методы:
        balance
        get_activation_summary
        get_number
    """
    session = requests.Session()

    __API_URL = "https://5sim.net/v1/"
    __available_countries = ['any', 'RU', 'KZ', 'UA', 'RO', 'UK', 'AR', 'BR', 'VN', 'HT', 'DE', 'GE', 'DO', 'EG', 'IL', 'ID', 'ES', 'KH', 'CA_V', 'KE', 'KG', 'CO', 'XK', 'LA', 'LV', 'LT', 'MY', 'MX', 'NL', 'NZ', 'PY', 'PL', 'PT', 'US', 'US3', 'PH', 'FI', 'FR', 'HR', 'CL', 'SE', 'EE',]
    __available_services = ['afghanista', 'albania', 'algeria', 'angola', 'antiguaandbarbuda', 'argentina', 'armenia', 'austria', 'azerbaijan', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'benin', 'bhutane', 'bih', 'bolivia', 'botswana', 'brazil', 'bulgaria', 'burkinafaso', 'burundi', 'cambodia', 'cameroon', 'canada', 'caymanislands', 'chad', 'china', 'colombia', 'congo', 'costarica', 'croatia', 'cyprus', 'czech', 'djibouti', 'dominicana', 'easttimor', 'ecuador', 'egypt', 'england', 'equatorialguinea', 'estonia', 'ethiopia', 'finland', 'france', 'frenchguiana', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'guadeloupe', 'guatemala', 'guinea', 'guineabissau', 'guyana', 'haiti', 'honduras', 'hungary', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy', 'ivorycoast', 'jamaica', 'jordan', 'kazakhstan', 'kenya', 'kuwait', 'laos', 'latvia', 'lesotho', 'libya', 'lithuania', 'luxembourg', 'macau', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'mauritania', 'mauritius', 'mexico', 'moldova', 'mongolia', 'montenegro', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nepal', 'netherlands', 'newzealand', 'nicaragua', 'nigeria', 'oman', 'pakistan', 'panama', 'papuanewguinea', 'paraguay', 'peru', 'philippines', 'poland', 'portugal', 'puertorico', 'qatar', 'reunion', 'romania', 'russia', 'rwanda', 'saintkittsandnevis', 'saintlucia', 'saintvincentandgrenadines', 'salvador', 'saudiarabia', 'senegal', 'serbia', 'slovakia', 'slovenia', 'somalia', 'southafrica', 'spain', 'srilanka', 'sudan', 'suriname', 'swaziland', 'sweden', 'syria', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'tit', 'togo', 'tunisia', 'turkey', 'turkmenistan', 'uae', 'uganda', 'uruguay', 'usa', 'uzbekistan', 'venezuela', 'vietnam', 'yemen', 'zambia', 'zimbabwe'] 
    __available_operators = ['any', '019', 'activ', 'altel', 'beeline', 'claro', 'globe', 'kcell', 'lycamobile', 'matrix', 'megafon', 'movistar', 'mts', 'orange', 'play', 'range1', 'redbull', 'redbullmobile', 'rostelecom', 'smart', 'sun', 'tele2', 'tigo', 'tmobile', 'tnt', 'virginmobile', 'yota']


    def __init__(self, api_key):
        """
        Параметры:
            api_key : str
                Ваш api ключ со страницы https://simsms.org/user/
        """
        self.api_key = api_key

        self.session.headers = {
            "Authorization": "Bearer {}".format(api_key)
        }

    def balance(self):
        """
        Баланс аккаунта
        Возрат:
            balane : float
        """
        params = {

        }
        path = "user/profile"
        balance = self.__request(path)["balance"]
        return float(balance)

    def get_activation_summary(self, country="any", operator="any"):
        self.__check_args(country=country, operator=operator)
            
        path = "guest/products/{}/{}".format(country, operator)
        return self.__request(path)

    def get_number(self, service, country="any", operator="any"):
        self.__check_args(country=country, operator=operator, service=service)

        path = "user/buy/activation/{/{}/{}".format(country, operator, service)
        return self.__request(path)

    def check_order(self, order_id):
        path = "user/check/{}".format(order_id)
        return self.__request(path)

    def set_status_ok(self, order_id):
        path = "user/finish/{}".format(order_id)
        return self.__request(path)

    def cancel_order(self, order_id):
        path = "user/cancel/{}".format(order_id)
        return self.__request(path)

    def number_already_used(self, number):
        path = "user/ban/{}".format(order_id)
        return self.__request(path)


    def __check_args(self, country=None, operator=None, service=None):
        if None != country and not country in self.__available_countries:
            raise exceptions.InvalidCountry()

        if None != operator and not operator in self.__available_operators:
            raise exceptions.InvalidOperator()

        if None != service and not service in self.__available_services:
            raise exceptions.InvalidService()


    def __request(self, path, params=None):
        response = self.session.get(self.__API_URL + path)

        try:
            response = response.json()
        except:
            raise exceptions.ApiError(response.text)
            

        return response