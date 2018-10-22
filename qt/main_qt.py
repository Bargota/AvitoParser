import sys
# ����������� ��� ���������
from main_qt import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ����� ����������� ������� ������� �� ������                     
        self.ui.pushButton.clicked.connect(self.DomainCheck)

    # ���� ������ ������� ������� �����������
    # ��� ������� �� ������                  
    def DomainCheck(self):
        pass

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())