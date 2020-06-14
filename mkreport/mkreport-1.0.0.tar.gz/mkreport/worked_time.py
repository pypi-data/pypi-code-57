import os
from . import print_error


class WorkedTime:
    DEFAULT_START_TIME = os.environ['DEFAULT_START_TIME']
    DEFAULT_END_TIME = os.environ['DEFAULT_END_TIME']

    def __init__(self):
        self.__times = self.__input_worked_times()
        self.__times_text = self.__format_report_time()

    @property
    def times_text(self):
        return self.__times_text

    def __format_report_time(self):
        return "【勤務時間】\n" + self.__times[0] + "-" + self.__times[1] + "\n"

    def __format_time(self, time):
        formated_time = time[:2] + ':' + time[2:]
        if formated_time[0] == '0':
            formated_time = formated_time[1:]
        return formated_time

    def __input_time(self, default_time, target_time):
        time = default_time
        while True:
            inp = input(
                target_time + 'を「hhmm」で入力してください(デフォルト「' + default_time + '」)\n')
            if not(inp):
                break
            elif inp.isdigit() and len(inp) == 4:
                time = inp
                break
            else:
                print_error.print_error('入力形式が正しくありません。')
        return time

    def __input_worked_times(self):
        worked_times = []
        while True:
            start_time = self.__input_time(self.DEFAULT_START_TIME, '勤務開始時間')
            end_time = self.__input_time(self.DEFAULT_END_TIME, '勤務終了時間')
            if start_time <= end_time:
                break
            else:
                print_error.print_error('勤務時間の入力が正しくありません。')
        worked_times.append(self.__format_time(start_time))
        worked_times.append(self.__format_time(end_time))
        return worked_times
