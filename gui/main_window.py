from input import Ui_MainWindow
from favorites import Ui_Dialog
from credenciais import Ui_Dialog_cred
import sys
import pymysql
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QAbstractTableModel, Qt


# Credentials to database connection ADD
hostname="localhost"
dbname="db"
username="root"
pwd=""

# connection = pymysql.connect(
#     host=hostname,
#     user=username,
#     password=pwd,
#     db=dbname
#     )

# cursor = connection.cursor()



class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self,parent=None):
        return self._data.shape[0]

    def columnCount(self,parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
    
    def hearderData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role ==Qt.DisplayRole:
            return self._data.columns[col]
        return None



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.exec_quer)
        self.ui.pushButton_2.clicked.connect(self.save_quer)
        self.ui.pushButton_3.clicked.connect(self.go_to_easy)
        self.ui.pushButton_4.clicked.connect(self.go_to_cred)


    def exec_quer(self):
        text = self.ui.plainTextEdit.toPlainText()
        df = pd.read_sql(text, connection)
        model = pandasModel(df)
        self.ui.tableView.setModel(model)
    
    def save_quer(self):
        text = self.ui.plainTextEdit.toPlainText()
        df = pd.read_sql(text, connection)
        print(df)
        df.to_csv(r'querie.csv')

    def go_to_easy(self):
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setFixedHeight(widget.currentWidget().frameGeometry().height())
        widget.setFixedWidth(widget.currentWidget().frameGeometry().width())

    def go_to_cred(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setFixedHeight(widget.currentWidget().frameGeometry().height())
        widget.setFixedWidth(widget.currentWidget().frameGeometry().width())


class Dialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.back.clicked.connect(self.back)
        self.ui.search.clicked.connect(self.fav_search)


    def back(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)
        widget.setFixedHeight(widget.currentWidget().frameGeometry().height())
        widget.setFixedWidth(widget.currentWidget().frameGeometry().width())

    def fav_search(self):
        quer_dic = {
            "Doses distribuídas para cada município" : "SELECT m.Nome, count(d.IdDose) FROM municipios m, `unidade saude` u, tem t, doses d, fica_no f WHERE m.Código=f.IdMunicipio AND f.IdUBS=u.IdUBS AND u.IdUBS=t.IdUBS AND t.IdDose=d.IdDose GROUP BY m.Nome;",
            "Relação Vacina e Origem":"SELECT lab.Nome AS Laboratório, lab.Pais, v.Nome AS Vacina, count(d.IdDose) AS `Doses aplicadas` FROM parcial.laboratorio lab, parcial.produzida_por  p, parcial.vacinas v, parcial.do_tipo dt, parcial.doses d WHERE lab.IdLaboratorio=p.IdLaboratorio AND v.IdVacina=p.IdVacina AND v.IdVacina=dt.IdVacina AND  d.IdDose=dt.IdDose GROUP BY v.Nome;",
            "Doses aplicadas por municípios" : "SELECT m.Nome, count(d.IdDose) FROM municipios m, habita_em h, pessoas p, aplicada_em a, doses d WHERE m.Código=h.IdMunicipio AND h.IdPessoa=p.Id AND p.Id=a.IdPessoa AND a.IdDose=d.IdDose GROUP BY m.Nome;",
            "Pessoas vacinadas por faixa etária" : "SELECT p1.Nome, p1.Data_de_Nascimento FROM pessoas p1  WHERE p1.Data_de_Nascimento  < \"1950-01-01\" AND EXISTS(SELECT * FROM aplicada_em a WHERE a.IdPessoa=p1.Id);",
            "Número de doses importadas da China" : "SELECT l.Pais, l.Nome, v.Nome, count(dt.idDose) FROM laboratorio l, produzida_por pp, vacinas v, do_tipo dt, doses d WHERE l.IdLaboratorio=pp.IdLaboratorio AND v.IdVacina=pp.IdVacina AND v.IdVacina=dt.IdVacina AND d.IdDose=dt.IdDose AND l.Pais=\"China\" GROUP BY l.Nome;",
            "Número de pessoas que receberam a 2° dose por município" : "SELECT m.Nome, count(p.Id) FROM parcial.pessoas p, parcial.aplicada_em ae, parcial.doses d, parcial.habita_em h, parcial.municipios m WHERE p.Id=ae.IdPessoa AND d.IdDose=ae.IdDose AND d.Número='    2ª Dose' AND p.Id = h.IdPessoa AND h.IdMunicipio = m.Código GROUP BY m.Código;"
        }
        pesquisa = self.ui.box.currentText()
        querie = quer_dic[pesquisa]
        df = pd.read_sql(querie, connection)
        model = pandasModel(df)
        self.ui.table.setModel(model)

class Dialog_cred(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_Dialog_cred()
        self.ui.setupUi(self)
        self.ui.search.clicked.connect(self.save_bt)


    def save_bt(self):
        global hostname
        global dbname
        global username
        global pwd
        global connection
        global cursor
        hostname = self.ui.plainTextEdit.toPlainText()
        dbname = self.ui.plainTextEdit_2.toPlainText()
        username = self.ui.plainTextEdit_3.toPlainText()
        pwd = self.ui.lineEdit.text()
        print(hostname)
        print(dbname)
        print(username)
        print(pwd)

        connection = pymysql.connect(
        host=hostname,
        user=username,
        password=pwd,
        db=dbname
        )
        cursor = connection.cursor()
        widget.setCurrentIndex(widget.currentIndex() + 1)
        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    main_win = MainWindow() 
    easy = Dialog()
    cred = Dialog_cred()
    widget.addWidget(cred)
    widget.addWidget(main_win)
    widget.addWidget(easy)
    widget.setFixedHeight(main_win.frameGeometry().height())
    widget.setFixedWidth(main_win.frameGeometry().width())
    widget.show()

    sys.exit(app.exec())
    