import datetime
import logging
from PyQt5 import QtCore
import kammanta.model
import kammanta.glob

TIME_MSECS_INT = 1000  # -one second
# if ct.ct_global.testing_bool: time_msecs_int = 50


class DoTimer(QtCore.QObject):
    update_signal = QtCore.pyqtSignal(bool)
    # -list has a collection of IDs, bool is whether it's a missed notification

    def __init__(self):
        super().__init__()

        logging.info("init for DoTimer")

        self.secs_elapsed_int = 0
        # self.start_secs_int = -1
        self.second_qtimer = None

    def start(self):
        self.stop()
        self.second_qtimer = QtCore.QTimer(self)
        self.second_qtimer.timeout.connect(self.timeout)
        # self.update_signal.emit(True)
        self.second_qtimer.start(TIME_MSECS_INT)

    def stop(self):
        if self.second_qtimer is not None and self.second_qtimer.isActive():
            self.second_qtimer.stop()
            logging.debug("do_timer stopped")
        self.secs_elapsed_int = 0
        self.update_signal.emit(False)
        # update_gui()

    def is_active(self):
        if self.second_qtimer is None:
            return False
        ret_is_active_bool = self.second_qtimer.isActive()
        return ret_is_active_bool

    def timeout(self):
        """
        Function is called every second
        """
        self.secs_elapsed_int += 1
        # logging.debug("time_remaining " + str(self.secs_remaining_int))
        """
        completed_bool = False
        if self.secs_elapsed_int == 0:
            completed_bool = True
            self.stop()
        """

        self.update_signal.emit(True)

    def get_formatted_time(self) -> str:
        minutes_int = self.secs_elapsed_int // 60
        seconds_remaining_int = self.secs_elapsed_int % 60
        formatted_time_str = str(minutes_int) + ":" + str(seconds_remaining_int).zfill(2)
        return formatted_time_str


"""
class DoTimer(QtCore.QObject):
    update_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.second_qtimer = None

    def start(self):
        self.move_files_and_show_notifications()
        self.start_shared_minute_timer()

    def move_files_and_show_notifications(self):
        now_pdt = datetime.datetime.now()
        tickler_list = gtd.model.tickler_files.get_all_items()
        for tickler_item in tickler_list:
            notification_time_pdt = tickler_item.get_reminder_time()
            if notification_time_pdt is None or now_pdt >= notification_time_pdt:
                # -if there is no notification time we move the item to the inbox
                # moving
                tickler_path_str = tickler_item.get_path()
                inbox_path_str = gtd.gtd_global.get_path(gtd.gtd_global.INBOX_DIR_STR)
                gtd.gtd_global.move_fd(tickler_path_str, inbox_path_str)

                # popup
                self.update_signal.emit(tickler_item.get_name())

    def start_shared_minute_timer(self):
        self.stop_second_timer()
        self.second_qtimer = QtCore.QTimer(self)
        self.second_qtimer.timeout.connect(self.second_timer_timeout)
        self.second_qtimer.start(1000)  # -one minute

    def stop_second_timer(self):
        if self.second_qtimer is not None and self.second_qtimer.isActive():
            self.second_qtimer.stop()

    def second_timer_timeout(self):
        logging.debug("second timer timeout")
        self.move_files_and_show_notifications()

"""
