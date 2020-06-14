from id_number_util import area_map as area
from datetime import datetime, timedelta

class IdNumber:

    __id = None
    __area_id = None
    __birth_year = None
    __birth_month = None
    __birth_day = None

    def __init__(self, id_number):
        self.__id = id_number
        self.__area_id = int(self.__id[0:6])
        self.__birth_year = int(self.__id[6:10])
        self.__birth_month = int(self.__id[10:12])
        self.__birth_day = int(self.__id[12:14])

    def get_id(self):
        return self.__id

    def get_area_name(self):
        return area.AREA_MAP[self.get_area_id()]

    def get_area_id(self):
        return self.__area_id

    def get_birthday(self):
        """通过身份证号获取出生日期"""
        return "{0}-{1}-{2}".format(self.__birth_year, self.__birth_month, self.__birth_day)

    def get_age(self):
        now = (datetime.now() + timedelta(days=1))
        year, month, day = now.year, now.month, now.day

        if year == self.__birth_year:
            return 0
        else:
            if self.__birth_month > month or (self.__birth_month == month and self.__birth_day > day):
                return year - self.__birth_year - 1
            else:
                return year - self.__birth_year

    def get_birth_year(self):
        return self.__birth_year

    def get_birth_month(self):
        return self.__birth_month

    def get_birth_day(self):
        return self.__birth_day

    def is_male(self):
        return bool(self.__id[16:17]) % 2