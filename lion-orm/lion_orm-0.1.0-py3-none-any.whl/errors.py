class InternalError(ValueError):
    """
    Просто внутренняя ошибка.
    """
    pass

class AttributeNotDefinedError(AttributeError):
    """
    Попытка совершить действие с атрибутом, который еще не определен.
    """
    pass

class SaveEmptyModelError(ValueError):
    """
    Попытка сохранить в базу информацию из экземпляра модели, не заполнив при этом все обязательные атрибуты.
    """
    pass

class AutoIncrementError(ValueError):
    """
    Внутренняя ошибка, связанная с отсутствием автоинкремента id.
    """
    pass

class GettingMultipleObjectsError(ValueError):
    """
    Попытка использования единичного доступа к объекту с использованием не уникального идентификатора.
    """
    pass

class DeleteDeletedError(ValueError):
    """
    Попытка удалить из базы уже удаленный объект.
    """
    pass

class EmptyDeleteError(ValueError):
    """
    Попытка удалить объект, который не представлен в базе.
    """
    pass

class UsingDeletedQuerySetError(ValueError):
    """
    Попытка совершить действие с удаленным набором объектов.
    """
    pass
