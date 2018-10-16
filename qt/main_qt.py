# -*-utf-8: -*-

import sys
import time

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import SIGNAL
from PyQt5.QtGui import QApplication, QMainWindow, QFont

from qt.test_form import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self,parent=None):
		QMainWindow.__init__(self)
		self.setupUi(self)

