import pip
import sys
import subprocess


class ElManager:
    """
        Менеджер для настройки микросервиса для ассистента Elitem.

        Использование::
            >>> ...
            >>> import elmicpy
            >>> manager = elmicpy.ElManager()
            >>> ...
    """

    ONE_EXECUTION = 0
    STREAMING_EXECUTION = 1
    STEP_POINT = 2
    SESSIONS_EXECUTION = 3
    CURRENT_EXECUTION = None

    EXECUTION_MICROS = [ONE_EXECUTION, STREAMING_EXECUTION,  STEP_POINT, SESSIONS_EXECUTION]
    LIST_PACKAGE = []
    LIST_PART = list()
    LIST_SESSIONS = list()
    STEP_TRANSMITTER = dict()

    COUNT_EXECUTION = False

    FEED_EXECUTION = False

    WELCOME_TEXT = ''

    def __init__(self, welcome=None):
        if welcome is not None:
            self.WELCOME_TEXT = welcome

    def set_executing(self, executing, *sessions, feed=None):
        """ Назначить исполнение

            Использование::
                >>> ...
                >>> manager.set_executting(manager.ONE_EXECUTION)
                >>> ...

            :param feed: Команда для исполнения
            :type feed: str
            :param executing: Название исполнния, взятые из класс ElManager. (Разрешено использовать цифры от 0 - 3)
            :type executing: int
            :param count_step: Кол-во шагов для пошагового исполнения
            :type count_step: int
        """
        if executing in self.EXECUTION_MICROS:
            for _ in self.EXECUTION_MICROS:
                if executing == _:
                    if executing == 1:
                        self.COUNT_EXECUTION = None
                        self.FEED_EXECUTION = feed
                    elif executing == 2:
                        self.FEED_EXECUTION = feed
                    elif executing == 3:
                        self.COUNT_EXECUTION = None
                        self.FEED_EXECUTION = feed
                        self.LIST_SESSIONS = sessions
                    else:
                        self.COUNT_EXECUTION = 1
                        self.FEED_EXECUTION = feed
                    self.CURRENT_EXECUTION = executing
            else:
                print("Указанное исполнение не существует.")

    def set_step(self, steps, parts, **transmitter):
        self.COUNT_EXECUTION = steps
        for part in parts:
            self.LIST_PART.append(part)
        if len(self.LIST_PART) != self.COUNT_EXECUTION:
            self.LIST_PART.clear()
            self.COUNT_EXECUTION = 0
            return "Несовпадение с выделенными частями"
        else:
            if transmitter:
                self.STEP_TRANSMITTER = transmitter.copy()

    def install(self, *packages):
        """ Установка бибилотек

        Использование::
            >>> ...
            >>> manager.install("name_package1", "name_package2")
            >>> ...

        :param packages: Список названий библиотек
        """
        for package in packages:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            self.LIST_PACKAGE.append(package)

    def uninstall(self):
        """ Удаление бибилотек """
        if self.LIST_PACKAGE:
            for package in self.LIST_PACKAGE:
                if hasattr(pip, 'main'):
                    pip.main(['uninstall', '-y', package])
                else:
                    pip._internal.main(['uninstall', '-y', package])

    @staticmethod
    def check_package():
        """ Проверка устаноленных бибилотек """
        return str(subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']))[2:-3].split("\\n")


class Session(ElManager):
    """
    Информация о сессии

    Использование::
        >>> ...
        >>>

    """
    CURRENT_SESSION = None

    NAME_SESSIONS = False
    MODULES_SESSIONS = False

    def set_step(self, steps, parts, **transmitter):
        self.COUNT_EXECUTION = steps
        for part in parts:
            self.LIST_PART.append(part)
        self.LIST_PART.append(self.MODULES_SESSIONS)
        if len(self.LIST_PART) != self.COUNT_EXECUTION:
            self.LIST_PART.clear()
            self.COUNT_EXECUTION = 0
            return "Несовпадение с выделенными частями"
        else:
            if transmitter:
                self.STEP_TRANSMITTER = transmitter.copy()


class NewSession(Session):
    def __init__(self, name_session, module, executing, feed, *extra_values):
        super().__init__()
        self.NAME_SESSIONS = name_session
        self.MODULES_SESSIONS = module
        self.CURRENT_EXECUTION = executing
        self.FEED_EXECUTION = feed
