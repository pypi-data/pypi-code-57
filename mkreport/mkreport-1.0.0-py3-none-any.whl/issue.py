import inquirer
from . import print_error


class Issue:
    def __init__(self, id=None, name=None, status=None, statuses=None):
        self.__id = id
        self.__name = name
        self.__status = status
        self.__statuses = statuses
        self.__comment = self.__input_comment()
        if id is not None:
            self.__time = self.__input_time()
            self.__new_status_id = self.__select_status()

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def comment(self):
        return self.__comment

    @property
    def time(self):
        return self.__time

    @property
    def new_status_id(self):
        return self.__new_status_id

    def status_changed(self):
        return self.__new_status_id != self.__statuses[str(self.__status)]

    def __input_comment(self):
        inp = input('日報に記載する作業内容を入力してください\n')
        return inp

    def __input_time(self):
        while True:
            inp = input('作業時間を入力してください\n')
            try:
                float(inp)
            except ValueError:
                print_error.print_error('数値を入力してください')
            else:
                if float(inp) >= 0:
                    break
                print_error.print_error('0以上の数値を入力してください')
        return float(inp)

    def __select_status(self):
        questions = [
            inquirer.List('status',
                          message="ステータスを選択してください。(現在のステータス{})".format(
                              str(self.__status)),
                          choices=self.__statuses,
                          default=str(self.__status),
                          ),
        ]
        answer = inquirer.prompt(questions)
        return self.__statuses[answer["status"]]
