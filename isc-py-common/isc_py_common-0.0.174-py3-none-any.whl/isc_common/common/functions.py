import re


def uncapitalize(str):
    return str[0:1].lower() + str[1:]


def dbl_qutes_str(str):
    return f'"{str}"'


def qutes_str(str):
    return f"'{str}'"


def delete_dbl_spaces(value):
    if value == None:
        return value
    return re.sub('\s+', ' ', value).strip();


def null2blanck(str):
    return '' if str == 'null' else str


class Common:
    @staticmethod
    def get_size_file_str(value):
        if value == 0:
            return ""

        if value > 0 and value <= 1024:
            return f'{value} Байт'

        if value > 1024 and value <= 1024 * 1024:
            return f'{round(value / 1024, 2)} КБайт'

        if value > 1024 * 1024 and value <= 1024 * 1024 * 1024:
            return f'{round(value / 1024 / 1024, 2)} МБайт'

        if value > 1024 * 1024 * 1024:
            return f'{round(value / 1024 / 1024 / 1024, 2)}  ГБайт'
        return value

    @staticmethod
    def arraund_error(error):
        str = '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        return f'\n{str}\n{error}\n{str}'
