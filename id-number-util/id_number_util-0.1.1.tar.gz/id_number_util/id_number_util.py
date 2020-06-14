import random
import re
from id_number_util import area_map as area, id_number
from datetime import datetime, timedelta

IdNumber = id_number.IdNumber

class IdNumberUtil:

    # 十五位身份证号表达式
    __ID_NUMBER_15_REGEX = r"^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$"

    # 十八位身份证号表达式
    __ID_NUMBER_18_REGEX = r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$'

    @staticmethod
    def generate_id_number(max_age=None, sex=None, area_list=None) -> IdNumber:
        # 随机生成一个区域码(6位数) 默认随机
        if area_list is None:
            area_list = list(area.AREA_MAP.keys())
        tmp_id_number = str(random.choice(area_list))

        # 限定出生日期范围(8位数) 默认不限制
        if max_age is None:
            start = datetime.strptime("19600101", "%Y%m%d")
        else:
            now = datetime.now()
            str_data = str(now.year - max_age) + str(now.month).zfill(2) + str(now.day).zfill(2)
            start = datetime.strptime(str_data, "%Y%m%d")
        end = datetime.now()
        birth_days = datetime.strftime(start + timedelta(random.randint(0, (end - start).days + 1)), "%Y%m%d")
        tmp_id_number += str(birth_days)

        # 顺序码(2位数)
        tmp_id_number += str(random.randint(10, 99))

        # 性别码(1位数) 默认随机
        if sex is None:
            sex = random.randint(0, 1)
        tmp_id_number += str(random.randrange(sex, 10, step=2))

        # 校验码(1位数)
        tmp_id_number += str(IdNumberUtil.__calculate_check_digit(tmp_id_number))
        return IdNumber(tmp_id_number)

    @staticmethod
    def __calculate_check_digit(tmp_id_number):
        """通过身份证号获取校验码"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(tmp_id_number[i])

        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'

    @staticmethod
    def verify_id(id_number_object: IdNumber):
        """校验身份证是否正确"""
        if re.match(IdNumberUtil.__ID_NUMBER_18_REGEX, id_number_object.get_id()):
            check_digit = IdNumberUtil.__calculate_check_digit(id_number_object.get_id())
            return str(check_digit) == id_number_object.get_id()[-1]
        else:
            return bool(re.match(IdNumberUtil.__ID_NUMBER_15_REGEX, id_number_object.get_id()))