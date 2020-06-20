class NoKey(Exception):
    """
    Не указан апи ключ
    """
    pass

class BadKey(Exception):
    """
    Неправильный апи ключ
    """
    pass


class NoAction(Exception):
    pass

class BadAction(Exception):
    pass


class ErrorSql(Exception):
    """
    Ошибка sql
    """
    pass

class NoMeans(Exception):
    """
    Недостаточно денег на балансе
    """
    pass 

class NoNumber(Exception):
    """
    Нет нужных номеров
    """
    pass 

class NoActivatorsRate(Exception):
    """
    Ставка активаторов выше ваше
    """
    pass

