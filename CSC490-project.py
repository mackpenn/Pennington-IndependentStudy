# MacKenzie Pennington - CSC490 Spring 2019

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QShortcut
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import pyqtSlot
from pynput import mouse, keyboard
from pynput.mouse import Button
import pandas
import time

# Class to load data table
class LoadTable(QtWidgets.QTableWidget):
    
    def __init__(self, parent=None, events=None):
        # Set initial rows, columns, and window size
        super(LoadTable, self).__init__(1, 4, parent)
        self.setFixedSize(402, 300)
        
        # Set horizontal headers
        headertitle = ("Device", "Coordinates", "Key", "Event")
        self.setHorizontalHeaderLabels(headertitle)
        self.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        # Set vertical headers
        self.verticalHeader().hide()

        # Disable item selection
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.cellChanged.connect(self._cellclicked)
        
        # Set shortcut keys, connect to button actions
        self.shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut.activated.connect(self.on_record_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut.activated.connect(self.on_stop_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        self.shortcut.activated.connect(self.on_play_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        self.shortcut.activated.connect(self.on_clear_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut.activated.connect(self.on_save_clicked)
        
        # Initialize mouse and keyboard listeners
        self.mouseListener = mouse.Listener(on_click = self.on_click,
                                            on_move = self.on_move,
                                            on_scroll = self.on_scroll)
        self.kbListener = keyboard.Listener(on_press = self.on_press,
                                            on_release = self.on_release)
            
        # Initialize mouse and keyboard controllers
        self.mouseController = mouse.Controller()
        self.kbController = keyboard.Controller()
        
        # If none exists, create a dataframe
        if events is None:
            self.events = pandas.DataFrame(columns=['Device', 'Coordinates', 'Key', 'Event'])
        else:
            self.events = events

    @QtCore.pyqtSlot(int, int)
    def _cellclicked(self, r, c):
        it = self.item(r, c)
        it.setTextAlignment(QtCore.Qt.AlignCenter)        

    # Clears dataframe
    @QtCore.pyqtSlot()
    def on_clear_clicked(self):
        print('Clear button clicked!')
        self.events = self.events.drop(self.events.index)
        while self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)
            
        print(self.events)
        
    # Starts mouse and keyboard listeners to record
    @QtCore.pyqtSlot()
    def on_record_clicked(self):
        self.mouseListener.start()
        self.kbListener.start()
        print('Recording...')
        
    # Tracks mouse movement
    def on_move(self, x, y):
        self.events = self.events.append(
                {'Device': 'Mouse',
                 'Coordinates': (x, y),
                 'Key': 'n/a',
                 'Event': 'Move'
                 }, ignore_index = True)

    # Tracks left/right mouse clicking/releasing
    def on_click(self, x, y, button, pressed):
        click = ""
        release = ""
        if "left" in str(button):
            click = "Left-clicked"
            release = "Released left-click"
        else:
            click = "Right-clicked"
            release = "Released right-click"
        
        self.events = self.events.append(
                {'Device': 'Mouse',
                 'Coordinates': (x,y),
                 'Key': 'n/a',
                 'Event': '{0}'.format(click if pressed else release)
                 }, ignore_index = True)

    # Tracks up/down scrolling
    def on_scroll(self, x, y, dx, dy):
        self.events = self.events.append(
                {'Device': 'Mouse',
                 'Coordinates': (x, y),
                 'Key': 'n/a',
                 'Event': 'Scrolled {0}'.format(
                         'down' if dy < 0 else 'up')
                 }, ignore_index = True)
                 
    # Tracks key presses
    def on_press(self, key):
        self.events = self.events.append(
                {'Device': 'Keyboard',
                 'Coordinates': 'n/a',
                 'Key': key,
                 'Event': 'Pressed key'
                 }, ignore_index = True)

    # Tracks key releases
    def on_release(self, key):
        self.events = self.events.append(
                {'Device': 'Keyboard',
                 'Coordinates': 'n/a',
                 'Key': key,
                 'Event': 'Released key'
                }, ignore_index = True)
        
    # Stops mouse and keyboard listeners, re-initializes them, prints recorded data
    @QtCore.pyqtSlot()
    def on_stop_clicked(self):
        if self.mouseListener.running:
            self.mouseListener.stop()
            self.mouseListener = mouse.Listener(on_click = self.on_click,
                                                on_move = self.on_move,
                                                on_scroll = self.on_scroll)
        if self.kbListener.running:
            self.kbListener.stop()
            self.kbListener = keyboard.Listener(on_press = self.on_press,
                                                on_release = self.on_release)
        
        print('Stopped recording!')
        self.printDataTable()
    
    # Starts controllers and plays all recorded actions
    @QtCore.pyqtSlot()
    def on_play_clicked(self):
        mouse = self.mouseController
        kb = self.kbController
        print('Replaying...')
        
        # Iterate through the rows, individually play mouse/keyboard actions
        for i, row in self.events.iterrows():
            if row['Device'] == 'Mouse':
                mouse.position = row['Coordinates']
                if row['Event'] == 'Left-clicked':
                    mouse.click(Button.left)
                elif row['Event'] == 'Released left-click':
                    mouse.release(Button.left)
                    time.sleep(1)
                elif row['Event'] == 'Right-clicked':
                    mouse.click(Button.right)
                elif row['Event'] == 'Released right-click':
                    mouse.release(Button.right)
                    time.sleep(1)
                elif row['Event'] == 'Scrolled down':
                    mouse.scroll(0, 1)
                elif row['Event'] == 'Scrolled up':
                    mouse.scroll(0, -1)
            else:
                if row['Event'] == 'Pressed key':
                    kb.press(row['Key'].char)
                elif row['Event'] == 'Released key':
                    kb.release(row['Key'].char)
                    
        print('Finished replay!')
        
    # Print dataframe to the window
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

# Class to initialize buttons
class Buttons(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Buttons, self).__init__(parent)    

        # Loads the GUI window
        table = LoadTable()

        # Initialize and connect buttons to actions
        clear_button = QtWidgets.QPushButton("Clear [Ctrl+E]")
        clear_button.clicked.connect(table.on_clear_clicked)

        record_button = QtWidgets.QPushButton("Record [Ctrl+R]")
        record_button.clicked.connect(table.on_record_clicked)
        
        stop_button = QtWidgets.QPushButton("Stop [Ctrl+Q]")
        stop_button.clicked.connect(table.on_stop_clicked)
        
        play_button = QtWidgets.QPushButton("Play [Ctrl+P]")
        play_button.clicked.connect(table.on_play_clicked)
        
        save_button = QtWidgets.QPushButton("Save [Ctrl+S]")
        save_button.clicked.connect(table.on_save_clicked)

        # Set button layout
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(clear_button, alignment=QtCore.Qt.AlignJustify)
        button_layout.addWidget(record_button, alignment=QtCore.Qt.AlignJustify)
        button_layout.addWidget(stop_button, alignment=QtCore.Qt.AlignJustify)
        button_layout.addWidget(play_button, alignment=QtCore.Qt.AlignJustify)
        button_layout.addWidget(save_button, alignment=QtCore.Qt.AlignJustify)

        # Set box containing buttons
        tablehbox = QtWidgets.QHBoxLayout()
        tablehbox.setContentsMargins(10, 10, 10, 10)
        tablehbox.addWidget(table)

        grid = QtWidgets.QGridLayout(self)
        grid.addLayout(button_layout, 0, 1)
        grid.addLayout(tablehbox, 0, 0)        

# Execute application
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Buttons()
    w.show()
    sys.exit(app.exec_())