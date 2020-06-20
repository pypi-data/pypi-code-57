# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        if not PreferencesDialog.objectName():
            PreferencesDialog.setObjectName(u"PreferencesDialog")
        PreferencesDialog.setWindowModality(Qt.WindowModal)
        PreferencesDialog.resize(660, 498)
        self.verticalLayout = QVBoxLayout(PreferencesDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(PreferencesDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabARMSim = QWidget()
        self.tabARMSim.setObjectName(u"tabARMSim")
        self.verticalLayout_4 = QVBoxLayout(self.tabARMSim)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox = QGroupBox(self.tabARMSim)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setTitle(u"ARMSim")
        self.groupBox.setFlat(False)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        self.labelARMSimCommand = QLabel(self.groupBox)
        self.labelARMSimCommand.setObjectName(u"labelARMSimCommand")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.labelARMSimCommand)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEditARMSimDirectory = QLineEdit(self.groupBox)
        self.lineEditARMSimDirectory.setObjectName(u"lineEditARMSimDirectory")
        self.lineEditARMSimDirectory.setText(u"")

        self.horizontalLayout.addWidget(self.lineEditARMSimDirectory)

        self.toolButtonARMSimDirectory = QToolButton(self.groupBox)
        self.toolButtonARMSimDirectory.setObjectName(u"toolButtonARMSimDirectory")

        self.horizontalLayout.addWidget(self.toolButtonARMSimDirectory)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label)

        self.lineEditARMSimCommand = QLineEdit(self.groupBox)
        self.lineEditARMSimCommand.setObjectName(u"lineEditARMSimCommand")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEditARMSimCommand)

        self.labelARMSimServer = QLabel(self.groupBox)
        self.labelARMSimServer.setObjectName(u"labelARMSimServer")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelARMSimServer)

        self.lineEditARMSimServer = QLineEdit(self.groupBox)
        self.lineEditARMSimServer.setObjectName(u"lineEditARMSimServer")
        self.lineEditARMSimServer.setText(u"")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEditARMSimServer)

        self.labelARMSimPort = QLabel(self.groupBox)
        self.labelARMSimPort.setObjectName(u"labelARMSimPort")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.labelARMSimPort)

        self.spinBoxARMSimPort = QSpinBox(self.groupBox)
        self.spinBoxARMSimPort.setObjectName(u"spinBoxARMSimPort")
        self.spinBoxARMSimPort.setMinimum(8000)
        self.spinBoxARMSimPort.setMaximum(9999)
        self.spinBoxARMSimPort.setValue(8010)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.spinBoxARMSimPort)

        self.useLabelsLabel = QLabel(self.groupBox)
        self.useLabelsLabel.setObjectName(u"useLabelsLabel")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.useLabelsLabel)

        self.useLabelsCheckBox = QCheckBox(self.groupBox)
        self.useLabelsCheckBox.setObjectName(u"useLabelsCheckBox")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.useLabelsCheckBox)


        self.verticalLayout_2.addLayout(self.formLayout)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tabARMSim)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setTitle(u"Gcc ARM")
        self.groupBox_2.setFlat(False)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.lineEditARMGccOptions = QLineEdit(self.groupBox_2)
        self.lineEditARMGccOptions.setObjectName(u"lineEditARMGccOptions")
        self.lineEditARMGccOptions.setText(u"")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.lineEditARMGccOptions)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEditARMGccCommand = QLineEdit(self.groupBox_2)
        self.lineEditARMGccCommand.setObjectName(u"lineEditARMGccCommand")
        self.lineEditARMGccCommand.setText(u"")

        self.horizontalLayout_2.addWidget(self.lineEditARMGccCommand)

        self.toolButtonARMGccCommand = QToolButton(self.groupBox_2)
        self.toolButtonARMGccCommand.setObjectName(u"toolButtonARMGccCommand")

        self.horizontalLayout_2.addWidget(self.toolButtonARMGccCommand)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.labelARMGccOptions = QLabel(self.groupBox_2)
        self.labelARMGccOptions.setObjectName(u"labelARMGccOptions")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.labelARMGccOptions)

        self.labelARMGccCommand = QLabel(self.groupBox_2)
        self.labelARMGccCommand.setObjectName(u"labelARMGccCommand")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.labelARMGccCommand)


        self.verticalLayout_3.addLayout(self.formLayout_2)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 43, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButtonARMSimRestoreDefaults = QPushButton(self.tabARMSim)
        self.pushButtonARMSimRestoreDefaults.setObjectName(u"pushButtonARMSimRestoreDefaults")

        self.horizontalLayout_3.addWidget(self.pushButtonARMSimRestoreDefaults)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.tabWidget.addTab(self.tabARMSim, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(PreferencesDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        QWidget.setTabOrder(self.lineEditARMSimServer, self.spinBoxARMSimPort)
        QWidget.setTabOrder(self.spinBoxARMSimPort, self.lineEditARMSimCommand)
        QWidget.setTabOrder(self.lineEditARMSimCommand, self.lineEditARMSimDirectory)
        QWidget.setTabOrder(self.lineEditARMSimDirectory, self.toolButtonARMSimDirectory)
        QWidget.setTabOrder(self.toolButtonARMSimDirectory, self.useLabelsCheckBox)
        QWidget.setTabOrder(self.useLabelsCheckBox, self.lineEditARMGccCommand)
        QWidget.setTabOrder(self.lineEditARMGccCommand, self.toolButtonARMGccCommand)
        QWidget.setTabOrder(self.toolButtonARMGccCommand, self.lineEditARMGccOptions)
        QWidget.setTabOrder(self.lineEditARMGccOptions, self.pushButtonARMSimRestoreDefaults)
        QWidget.setTabOrder(self.pushButtonARMSimRestoreDefaults, self.tabWidget)

        self.retranslateUi(PreferencesDialog)
        self.buttonBox.accepted.connect(PreferencesDialog.accept)
        self.buttonBox.rejected.connect(PreferencesDialog.reject)

        QMetaObject.connectSlotsByName(PreferencesDialog)
    # setupUi

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QCoreApplication.translate("PreferencesDialog", u"QtARMSim Preferences", None))
        self.labelARMSimCommand.setText(QCoreApplication.translate("PreferencesDialog", u"ARMSim directory", None))
        self.toolButtonARMSimDirectory.setText(QCoreApplication.translate("PreferencesDialog", u"...", None))
        self.label.setText(QCoreApplication.translate("PreferencesDialog", u"Command line", None))
        self.labelARMSimServer.setText(QCoreApplication.translate("PreferencesDialog", u"Server", None))
        self.labelARMSimPort.setText(QCoreApplication.translate("PreferencesDialog", u"Port", None))
        self.useLabelsLabel.setText(QCoreApplication.translate("PreferencesDialog", u"Use labels", None))
#if QT_CONFIG(tooltip)
        self.useLabelsCheckBox.setToolTip(QCoreApplication.translate("PreferencesDialog", u"Use labels on the disassembled code instead of the corresponding numeric value", None))
#endif // QT_CONFIG(tooltip)
        self.toolButtonARMGccCommand.setText(QCoreApplication.translate("PreferencesDialog", u"...", None))
        self.labelARMGccOptions.setText(QCoreApplication.translate("PreferencesDialog", u"Options", None))
        self.labelARMGccCommand.setText(QCoreApplication.translate("PreferencesDialog", u"Command line", None))
        self.pushButtonARMSimRestoreDefaults.setText(QCoreApplication.translate("PreferencesDialog", u"Restore Defaults", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabARMSim), QCoreApplication.translate("PreferencesDialog", u"ARMSim", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "")
    # retranslateUi

