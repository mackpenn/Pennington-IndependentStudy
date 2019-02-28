# MacKenzie Pennington - CSC490 Spring 2019

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from time import sleep
from pynput import mouse
import pandas


class LoadTable(QtWidgets.QTableWidget):
    
    def __init__(self, parent=None):
        super(LoadTable, self).__init__(3, 3, parent)
        headertitle = ("Device", "Coordinates", "Event")
        self.setFixedSize(340, 280)
        self.setHorizontalHeaderLabels(headertitle)
        self.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.verticalHeader().hide()
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.setColumnWidth(0, 130)

        self.cellChanged.connect(self._cellclicked)
        
        self.mouseListener = mouse.Listener(on_click = self.on_click)
        self.keyEvents = pandas.DataFrame(columns=['Device', 'Coordinates', 'Event'])

    @QtCore.pyqtSlot(int, int)
    def _cellclicked(self, r, c):
        it = self.item(r, c)
        it.setTextAlignment(QtCore.Qt.AlignCenter)        

    @QtCore.pyqtSlot()
    def on_clear_clicked(self):
        print('Clear button clicked!')
        while self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)
        
    @QtCore.pyqtSlot()
    def on_record_clicked(self):
#        testList1 = ["mouse", "keyboard", "mouse"]
#        testList2 = [(2,3), "-", (4,5)]
#        testList3 = ["click", "spacebar", "right-click"]
#        row = -1
#
#        for x in testList1:
#            self.setItem(row+1, 0, QTableWidgetItem(str(testList1[x])))
#        
#        for y in testList2:
#            self.setItem(row+1, 1, QTableWidgetItem(str(testList2[y]))
#            
#        for z in testList3:
#            self.setItem(row+1, 2, QTableWidgetItem(str(testList3[z])))
        
        self.mouseListener.start()
        print('Recording...')
      
    def on_move(x, y):
        print('Pointer moved to {0}'.format(
                (x, y)))

    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format(
                'Pressed' if pressed else 'Released',
                (x, y)))
        if not pressed:
            # Stop listener
            return False

    def on_scroll(x, y, dx, dy):
        print('Scrolled {0} at {1}'.format(
                'down' if dy < 0 else 'up',
                (x, y)))

    # Collect events until released
    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()
        
    @QtCore.pyqtSlot()
    def on_stop_clicked(self):
        
        if self.mouseListener.running:
            self.mouseListener.stop()
            
            self.mouseListener = mouse.Listener(on_click = self.on_click)
        
        print('Stopped recording!')
        
        
    @QtCore.pyqtSlot()
    def on_save_clicked(self):
        ##TO-DO
        print('Save button clicked!')


class Buttons(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Buttons, self).__init__(parent)    

        table = LoadTable()

        clear_button = QtWidgets.QPushButton("Clear")
        clear_button.clicked.connect(table.on_clear_clicked)

        record_button = QtWidgets.QPushButton("Record")
        record_button.clicked.connect(table.on_record_clicked)
        
        stop_button = QtWidgets.QPushButton("Stop")
        stop_button.clicked.connect(table.on_stop_clicked)
        
        save_button = QtWidgets.QPushButton("Save")
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
