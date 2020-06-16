import os
import pathlib
import time

import gridfs
import pymongo
import requests
from PySide2.QtWidgets import *

import vmi
import vmi.application.skyward

case_db = vmi.application.skyward.case_db
order_db = vmi.application.skyward.order_db
user_db = vmi.application.skyward.user_db
role_customer_db = vmi.application.skyward.role_customer_db
role_sales_worker_db = vmi.application.skyward.role_sales_worker_db
role_product_designer_db = vmi.application.skyward.role_product_designer_db
role_quality_inspector_db = vmi.application.skyward.role_quality_inspector_db
dicom_fs = vmi.application.skyward.dicom_fs
vti_fs = vmi.application.skyward.vti_fs
vtp_fs = vmi.application.skyward.vtp_fs
stl_fs = vmi.application.skyward.stl_fs





if __name__ == '__main__':
    vmi.app.setApplicationName('Skyorder')
    vmi.app.setApplicationVersion('1.0')
    vmi.app.setQuitOnLastWindowClosed(False)

    client = pymongo.MongoClient('mongodb://root:medraw123@med-3d.top:27018/admin', 27017)
    database = client.skyward
    case_db = database.get_collection('case')
    order_db = database.get_collection('order')
    stl_fs = gridfs.GridFS(database, collection='stl')

    tray_icon_menu = QMenu()
    tray_icon_menu.addAction('待检生产单').triggered.connect(find_order_released)
    tray_icon_menu.addAction('在产生产单').triggered.connect(find_order_inspected)
    tray_icon_menu.addSeparator()
    tray_icon_menu.addAction('关于').triggered.connect(vmi.app_about)
    tray_icon_menu.addSeparator()
    tray_icon_menu.addAction('退出').triggered.connect(vmi.app.quit)

    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QWidget().style().standardIcon(QStyle.SP_ComputerIcon))
    tray_icon.setToolTip('{} {}'.format(vmi.app.applicationName(), vmi.app.applicationVersion()))
    tray_icon.setContextMenu(tray_icon_menu)
    tray_icon.activated.connect(tray_icon_activated)
    tray_icon.show()

    vmi.app.exec_()
    vmi.appexit()
