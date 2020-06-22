import enum
import logging
import sys
import os.path
import os
import datetime
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
import kammanta.model
import kammanta.glob


class CalendarCw(QtWidgets.QWidget):
    def __init__(self, i_days_delta: int):
        super().__init__()
        # self.setFixedHeight(340)

        self.days_delta_int = i_days_delta

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        datetime_hbox_l3 = QtWidgets.QHBoxLayout()
        vbox_l2.addLayout(datetime_hbox_l3)

        self.calendar_widget = QtWidgets.QCalendarWidget()
        datetime_hbox_l3.addWidget(self.calendar_widget)
        today_qdate = QtCore.QDate.currentDate()
        self.calendar_widget.setMinimumDate(today_qdate)
        new_qtf = self.calendar_widget.dateTextFormat(today_qdate)
        new_qtf.setFontUnderline(True)
        # -other changes can be made: https://doc.qt.io/qt-5/qtextcharformat.html
        self.calendar_widget.setDateTextFormat(today_qdate, new_qtf)
        # The following doesn't help:
        # self.calendar_widget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.SingleLetterDayNames)
        # self.calendar_widget.setFixedWidth(260)
        """
        date = QtCore.QDate()
        old_datetextformat = self.calendar_widget.dateTextFormat(date)
        logging.info("fontLetterSpacing =" + str(old_datetextformat.fontLetterSpacing()))
        self.calendar_widget.setStyleSheet("* {padding-left: 0px}")
        """
        # It's possible to reduce the font size, but this is not a solution i'm happy with

        vbox_l4 = QtWidgets.QVBoxLayout()
        datetime_hbox_l3.addLayout(vbox_l4)
        vbox_l4.addStretch(1)
        self.nr_of_days_qll = QtWidgets.QLabel("Nr of days")
        vbox_l4.addWidget(self.nr_of_days_qll)
        self.nr_of_days_qsb = QtWidgets.QSpinBox()
        vbox_l4.addWidget(self.nr_of_days_qsb)
        vbox_l4.addStretch(1)
        self.hour_qll = QtWidgets.QLabel("Hours")
        vbox_l4.addWidget(self.hour_qll)
        self.hour_qte = QtWidgets.QTimeEdit()
        vbox_l4.addWidget(self.hour_qte)
        self.hour_qte.setDisplayFormat("HH:mm")
        vbox_l4.addStretch(1)
        self.today_now_qpb = QtWidgets.QPushButton("Today/Now")
        vbox_l4.addWidget(self.today_now_qpb)
        self.today_now_qpb.clicked.connect(self.on_today_now_clicked)
        vbox_l4.addStretch(1)

        self.reset_datetime()

    def reset_datetime(self):
        today_qdate = QtCore.QDate.currentDate()
        qdate = today_qdate.addDays(self.days_delta_int)
        self.calendar_widget.setSelectedDate(qdate)

    def on_today_now_clicked(self):
        today_qd = QtCore.QDate.currentDate()
        self.calendar_widget.setSelectedDate(today_qd)

    def get_datetime_string(self) -> str:
        qt_date = self.calendar_widget.selectedDate()
        qt_time = self.hour_qte.time()
        qt_dt = QtCore.QDateTime(qt_date, qt_time)
        datetime_str = qt_dt.toString(kammanta.glob.QT_DATETIME_FORMAT_STR)
        logging.debug("datetime_str = " + datetime_str)

        dt_py = datetime.datetime.strptime(datetime_str, kammanta.glob.PY_DATETIME_FILENAME_FORMAT_STR)
        #####self.calendar_widget.setDateTextFormat(gtd.model.DATETIME_FORMAT_STR)

        return datetime_str


class CalendarInputDialog(QtWidgets.QDialog):
    def __init__(self, i_days_delta: int):
        super().__init__()
        # , *args, **kwargs

        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        self.setSizeGripEnabled(True)
        self.setWindowTitle("Calendar input")

        vbox_l1 = QtWidgets.QVBoxLayout(self)

        self.calendar_cw = CalendarCw(i_days_delta)
        # QtWidgets.QCalendarWidget()
        vbox_l1.addWidget(self.calendar_cw)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox_l1.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    @staticmethod
    def get_date_time_string(i_days_delta: int) -> (str, bool):
        cal_dlg = CalendarInputDialog(i_days_delta)
        dialog_result = cal_dlg.exec_()
        if dialog_result == QtWidgets.QDialog.Accepted:
            # selected_qdate = cal_dlg.calendar_cw.calendar_widget.selectedDate()
            # date_str = selected_qdate.toString(gtd.model.QT_DATETIME_FORMAT_STR)
            date_str = cal_dlg.calendar_cw.get_datetime_string()
            return (date_str, True)
        return ("", False)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = QtWidgets.QApplication(sys.argv)

    # Existing file
    date_str = CalendarInputDialog.get_date_time_string(4)
    logging.debug(date_str)

    sys.exit()



