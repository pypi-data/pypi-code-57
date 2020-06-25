from PyQt5.QtCore import QAbstractItemModel, QAbstractProxyModel
from PyQt5.QtWidgets import QFileDialog

class VirtualIteModel(QAbstractProxyModel):


    def rowCount(self, parent=None, *args, **kwargs):
        print("asd")

class VirtualDirectoryDialog(QFileDialog):

    def __init__(self, virtual_directory_device):
        print(virtual_directory_device)
        QFileDialog.__init__(self)
        print(self.proxyModel())

    def setProxyModel(self, QAbstractProxyModel):
        print("now")