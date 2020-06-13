

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


context = None
def init(context_):
    global context
    context = context_


class MyTest:
    def test(self):
        print("Hello Test222!")


config = {
    'pluginid': 'Core::ATest',
    "extensions" : [
        {
            "name": "PL::Test1",
            "impl": MyTest()
        }
    ]
}