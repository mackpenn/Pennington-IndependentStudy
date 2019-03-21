# MacKenzie Pennington - CSC490 Spring 2019

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QShortcut
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import pyqtSlot
from pynput import mouse, keyboard
import pandas


class LoadTable(QtWidgets.QTableWidget):
    
    def __init__(self, parent=None):
        super(LoadTable, self).__init__(1, 3, parent)
        self.setFixedSize(350, 280)
        
        headertitle = ("Device", "Coordinates", "Event")
        self.setHorizontalHeaderLabels(headertitle)
        self.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        self.verticalHeader().hide()

        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.setColumnWidth(0, 130)

        self.cellChanged.connect(self._cellclicked)
        
        self.shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut.activated.connect(self.on_record_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut.activated.connect(self.on_stop_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        self.shortcut.activated.connect(self.on_clear_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut.activated.connect(self.on_save_clicked)
        
        self.mouseListener = mouse.Listener(on_click = self.on_click,
                                            on_move = self.on_move,
                                            on_scroll = self.on_scroll)
        self.events = pandas.DataFrame(columns=['Device', 'Coordinates', 'Event'])

    @QtCore.pyqtSlot(int, int)
    def _cellclicked(self, r, c):
        it = self.item(r, c)
        it.setTextAlignment(QtCore.Qt.AlignCenter)        

    @QtCore.pyqtSlot()
    def on_clear_clicked(self):
        print('Clear button clicked!')
        self.events = self.events.drop(self.events.index)
        while self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)
            
        print(self.events)
        
    @QtCore.pyqtSlot()
    def on_record_clicked(self):
        self.mouseListener.start()
        print('Recording...')
        
    def on_move(self, x, y):
        self.events = self.events.append(
                {'Device': 'Mouse',
                 'Coordinates': (x, y),
                 'Event': 'Move'
                 }, ignore_index = True)

    def on_click(self, x, y, button, pressed):
        self.events = self.events.append(
                {'Device': 'Mouse',
                 'Coordinates': (x,y),
                 'Event': '{0}'.format(
                         'Clicked' if pressed else 'Released')
                 }, ignore_index = True)

    def on_scroll(self, x, y, dx, dy):
        self.events = self.events.append(
                {'Device': 'Mouse',
                 'Coordinates': (x, y),
                 'Event': 'Scrolled {0}'.format(
                         'down' if dy < 0 else 'up')
                 }, ignore_index = True)
        
    @QtCore.pyqtSlot()
    def on_stop_clicked(self):
        if self.mouseListener.running:
            self.mouseListener.stop()
            self.mouseListener = mouse.Listener(on_click = self.on_click)
        
        print('Stopped recording!')
        self.printDataTable()
        print(self.events)
        
    @QtCore.pyqtSlot()
    def printDataTable(self):
        self.setColumnCount(len(self.events.columns))
        self.setRowCount(len(self.events.index))
        
        for i in range(len(self.events.index)):
            for j in range(len(self.events.columns)):
                self.setItem(i, j, QTableWidgetItem(str(self.events.iloc[i, j])))
        
    @QtCore.pyqtSlot()
    def on_save_clicked(self):
        ##TO-DO
        print('Save button clicked!')

class Buttons(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Buttons, self).__init__(parent)    

        table = LoadTable()

        clear_button = QtWidgets.QPushButton("Clear [Ctrl+E]")
        clear_button.clicked.connect(table.on_clear_clicked)

        record_button = QtWidgets.QPushButton("Record [Ctrl+R]")
        record_button.clicked.connect(table.on_record_clicked)
        
        stop_button = QtWidgets.QPushButton("Stop [Ctrl+Q]")
        stop_button.clicked.connect(table.on_stop_clicked)
        
        save_button = QtWidgets.QPushButton("Save [Ctrl+S]")
        save_button.clicked.connect(table.on_save_clicked)

        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(clear_button, alignment=QtCore.Qt.AlignJustify)
        button_layout.addWidget(record_button, alignment=QtCore.Qt.AlignJustify)
        button_layout.addWidget(stop_button, alignment=QtCore.Qt.AlignJustify)
        button_layout.addWidget(save_button, alignment=QtCore.Qt.AlignJustify)

        tablehbox = QtWidgets.QHBoxLayout()
        tablehbox.setContentsMargins(10, 10, 10, 10)
        tablehbox.addWidget(table)

        grid = QtWidgets.QGridLayout(self)
        grid.addLayout(button_layout, 0, 1)
        grid.addLayout(tablehbox, 0, 0)        


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Buttons()
    w.show()
    sys.exit(app.exec_())