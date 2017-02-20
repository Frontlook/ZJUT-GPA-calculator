# coding=gbk
import sys
import sdu
import locale
from PyQt4.QtCore import *
from PyQt4 import QtCore, QtGui, uic
reload(sys)
sys.setdefaultencoding("utf-8")

mycode = locale.getpreferredencoding()
code = QTextCodec.codecForName(mycode)
QTextCodec.setCodecForLocale(code)
QTextCodec.setCodecForTr(code)
QTextCodec.setCodecForCStrings(code)

qtCreatorFile = "login.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.denglu.clicked.connect(self.CalculateTax)

    def CalculateTax(self):
        self.text.setText('')   # clean text browser
        xuehao = (self.xuehao.text())
        mima = (self.mima.text())
        sdu1 = sdu.SDU(xuehao, mima)
        sdu1.getGrades()
        for i in range(sdu1.one.__len__()):
            self.text.append(sdu1.one[i]+'\t'+sdu1.two[i]+'\t'+sdu1.three[i]+'\t'+sdu1.four[i])
            i += 1

        gpa = sdu1.getGrade()
        self.text.append('')
        self.text.append(u"平均绩点为：<strong>"+str(gpa)+"<strong>")
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

