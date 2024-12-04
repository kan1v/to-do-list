import sqlite3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_mainWindow
import sqlite3
from PyQt5.QtWidgets import QMessageBox

class ToDoList(QtWidgets.QMainWindow):
    def __init__(self):
        super(ToDoList, self).__init__()
        self.gui = Ui_mainWindow()
        self.gui.setupUi(self)
        self.init_UI()
        self.load_base()

    def init_UI(self):
        self.setWindowTitle("To-Do List")
        self.gui.btn_delete.clicked.connect(self.delete_task)
        self.gui.btn_save.clicked.connect(self.add_task)
        self.gui.btn_complete.clicked.connect(self.completed_task)

    def load_base(self):
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        cursor.execute("SELECT name_task FROM Tasks")
        tasks = cursor.fetchall()

        for task in tasks:
            self.gui.listbox.addItem(task[0])

        connection.close()


    def add_task(self):
        new_task = self.gui.input_line.text()
        if new_task:
            connection = sqlite3.connect("tasks.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Tasks(name_task) VALUES (?)",(new_task,))
            connection.commit()

            connection.close()

            self.gui.input_line.clear()
            self.gui.listbox.clear()

            self.load_base()




    def completed_task(self):
        selected_item = self.gui.listbox.currentItem()

        if selected_item:
            task_name = selected_item.text()

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Задача '{task_name}' выполнена! Молодец!")
            msg.setWindowTitle("Успех")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


            connection = sqlite3.connect("tasks.db")
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Tasks WHERE name_task = ?", (task_name,))
            connection.commit()

            row = self.gui.listbox.row(selected_item)
            self.gui.listbox.takeItem(row)

            connection.close()




    def delete_task(self):
        selected_item = self.gui.listbox.currentItem()

        if selected_item:
            task_name = selected_item.text()
        connection = sqlite3.connect("tasks.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Tasks WHERE name_task = ?", (task_name,))
        connection.commit()

        row = self.gui.listbox.row(selected_item)
        self.gui.listbox.takeItem(row)

        connection.close()














app = QtWidgets.QApplication([])
application = ToDoList()
application.show()
sys.exit(app.exec_())