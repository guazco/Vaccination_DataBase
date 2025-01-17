# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'favorites.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(780, 586)
        font = QtGui.QFont()
        font.setFamily("Wingdings 3")
        font.setPointSize(18)
        Dialog.setFont(font)
        Dialog.setAutoFillBackground(False)
        Dialog.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(65, 80, 209), stop:1 rgb(36, 0, 157));")
        self.table = QtWidgets.QTableView(Dialog)
        self.table.setGeometry(QtCore.QRect(80, 251, 481, 311))
        self.table.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.table.setObjectName("table")
        self.box = QtWidgets.QComboBox(Dialog)
        self.box.setGeometry(QtCore.QRect(80, 220, 481, 22))
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(11)
        self.box.setFont(font)
        self.box.setStyleSheet("background-color: rgb(255, 255, 255,100%);")
        self.box.setObjectName("box")
        self.box.addItem("")
        self.box.addItem("")
        self.box.addItem("")
        self.box.addItem("")
        self.box.addItem("")
        self.box.addItem("")
        self.back = QtWidgets.QPushButton(Dialog)
        self.back.setGeometry(QtCore.QRect(20, 20, 51, 41))
        font = QtGui.QFont()
        font.setFamily("Wingdings 3")
        font.setPointSize(11)
        self.back.setFont(font)
        self.back.setStyleSheet("background-color: rgb(227, 227, 227);\n"
"border-style: solid;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"border-width: 2px;")
        self.back.setObjectName("back")
        self.search = QtWidgets.QPushButton(Dialog)
        self.search.setGeometry(QtCore.QRect(580, 210, 121, 41))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.search.setFont(font)
        self.search.setStyleSheet("background-color: rgb(227, 227, 227);\n"
"border-style: solid;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"border-width: 2px;")
        self.search.setObjectName("search")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(600, 310, 101, 161))
        self.label_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("aligator.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.box.setItemText(0, _translate("Dialog", "Doses distribuídas para cada município"))
        self.box.setItemText(1, _translate("Dialog", "Relação Vacina e Origem"))
        self.box.setItemText(2, _translate("Dialog", "Doses aplicadas por municípios"))
        self.box.setItemText(3, _translate("Dialog", "Pessoas vacinadas por faixa etária"))
        self.box.setItemText(4, _translate("Dialog", "Número de doses importadas da China"))
        self.box.setItemText(5, _translate("Dialog", "Número de pessoas que receberam a 2° dose por município"))
        self.back.setText(_translate("Dialog", "Z"))
        self.search.setText(_translate("Dialog", "Search"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())