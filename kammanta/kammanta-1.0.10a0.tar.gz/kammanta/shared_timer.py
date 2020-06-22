import datetime
import logging
from PyQt5 import QtCore
import kammanta.model
import kammanta.glob


class SharedMinuteTimer(QtCore.QObject):
    tickler_notification_signal = QtCore.pyqtSignal(str)
    # -for updating the GUI, only emitted when a GUI update is needed

    clock_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.minute_qtimer = None

    def start(self):
        self.move_files_and_show_notifications()
        self.clock_update()
        self.start_minute_timer()

    def move_files_and_show_notifications(self):
        now_pdt = datetime.datetime.now()
        tickler_list = kammanta.model.tickler_files.get_all_items()
        for tickler_item in tickler_list:
            notification_time_pdt = tickler_item.get_reminder_time()
            if notification_time_pdt is None or now_pdt >= notification_time_pdt:
                # -if there is no notification time we move the item to the inbox
                # moving
                tickler_path_str = tickler_item.get_path()
                tickler_name_str = tickler_item.get_name()
                inbox_path_str = kammanta.glob.get_path(kammanta.glob.INBOX_DIR_STR)
                kammanta.glob.move_fd(tickler_path_str, inbox_path_str)

                # popup
                self.tickler_notification_signal.emit(tickler_name_str)

    def start_minute_timer(self):
        self.stop_shared_minute_timer()
        self.minute_qtimer = QtCore.QTimer(self)
        self.minute_qtimer.timeout.connect(self._shared_minute_timer_timeout)
        self.minute_qtimer.start(60 * 1000)  # -one minute

    def stop_shared_minute_timer(self):
        if self.minute_qtimer is not None and self.minute_qtimer.isActive():
            self.minute_qtimer.stop()

    def _shared_minute_timer_timeout(self):
        logging.debug("timeout")
        self.move_files_and_show_notifications()
        self.clock_update()

    def clock_update(self):
        self.clock_signal.emit()


