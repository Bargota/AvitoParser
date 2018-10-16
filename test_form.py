import sys
import PyQt5
import pyqt5_tools



class Example(PyQt5.QtWidgets):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):               
        
        self.resize(250, 150)
        self.center()
        
        self.setWindowTitle('Center')    
        self.show()
        
    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

