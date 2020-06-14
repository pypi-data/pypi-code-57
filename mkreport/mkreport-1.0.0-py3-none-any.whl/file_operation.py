import datetime
import os
import pyperclip
import sys
from . import print_error


class FileOperation:
    REPORTER = os.environ['REPORTER']
    today = datetime.date.today()

    def __init__(self):
        self.__dir_path = self.__build_dir_path()
        self.__file_path = self.__build_file_path()
        self.__check_exist_report()

    def build_report_content(self, worked_time, worked_ticket):
        module_dir = os.path.dirname(__file__)
        content_path = os.path.join(module_dir, 'report_content.txt')
        report_content = open(content_path, 'r').read().format(
            reporter=self.REPORTER,
            date=self.__build_time(),
            worked_time=worked_time,
            worked_ticket=worked_ticket,
            comment=self.__build_comment()
        )
        self.__content = report_content

    def make_report(self):
        os.makedirs(self.__dir_path, exist_ok=True)
        f = open(self.__file_path, 'w')
        f.write(self.__content)
        print('日報を作成しました。')
        print(self.__file_path)
        f.close()
        pyperclip.copy(self.__content)

    def __build_comment(self):
        input_comment = self.__input_comment()
        return "" if not input_comment else "【ひとこと】\n" + input_comment

    def __build_dir_path(self):
        year = str(self.today.year)
        month = str(self.today.month)
        dir_path = "./daily_report/" + year + "/" + month + "/"
        return dir_path

    def __build_file_path(self):
        return self.__dir_path + str(self.today.day) + ".txt"

    def __build_time(self):
        day_of_week_list = ["月", "火", "水", "木", "金", "土", "日"]
        day_of_week = day_of_week_list[self.today.weekday()]
        return self.today.strftime('%-m/%-d') + "(" + day_of_week + ")"

    def __check_exist_report(self):
        if os.path.isfile(self.__file_path):
            print_error.print_error('すでに本日の日報があります。')
            sys.exit()

    def __input_comment(self):
        comment = ""
        while True:
            inp = input('日報の最後に記載する一言を入力してください(qを入力すると終了)\n')
            if inp == 'q':
                break
            else:
                comment += inp + "\n"
        return comment
