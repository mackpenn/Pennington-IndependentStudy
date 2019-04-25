
# MacKenzie Pennington - CSC490 Spring 2019

import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, QShortcut, QLabel, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import pyqtSlot
from pynput import mouse, keyboard
from pynput.mouse import Button
import pandas
import time
import re

# Class to load data table
class LoadTable(QtWidgets.QTableWidget):
    
    def __init__(self, parent=None, df=None):
        # Set initial rows, columns, and window size
        super(LoadTable, self).__init__(1, 4, parent)
        self.setMinimumSize(405, 350)
        
        # Set horizontal headers
        headertitle = ("Device", "Coordinates", "Key", "Event")
        self.setHorizontalHeaderLabels(headertitle)
        self.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)

        # Set vertical headers
        self.verticalHeader().hide()

        # Specify how rows should be selected
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.cellChanged.connect(self._cellclicked)
        
        # Set shortcut keys, connect to button actions
        self.shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcut.activated.connect(self.on_record_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        self.shortcut.activated.connect(self.on_stop_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        self.shortcut.activated.connect(self.on_play_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+I"), self)
        self.shortcut.activated.connect(self.on_insert_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(self.on_clear_one_clicked)
        self.shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        self.shortcut.activated.connect(self.on_clear_all_clicked)
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
        if df is None:
            self.df = pandas.DataFrame(columns=['Device', 'Coordinates', 'Key', 'Event'])
        else:
            self.df = df

    @QtCore.pyqtSlot(int, int)
    def _cellclicked(self, r, c):
        it = self.item(r, c)
        it.setTextAlignment(QtCore.Qt.AlignCenter)        

    # Clears dataframe
    @QtCore.pyqtSlot()
    def on_clear_all_clicked(self):
        print('Clear All button clicked!')
        self.df = self.df.drop(self.df.index)
        while self.rowCount() > 0:
            self.removeRow(self.rowCount()-1)
            
        print(self.df)
       
    # Clears one selected row of dataframe
    @QtCore.pyqtSlot()
    def on_clear_one_clicked(self):
        self.removeRow(self.currentRow())
        print('Clear One button clicked!')
        
    # Starts mouse and keyboard listeners to record
    @QtCore.pyqtSlot()
    def on_record_clicked(self):
        self.mouseListener.start()
        self.kbListener.start()
        print('Recording...')
        
    # Tracks mouse movement
    def on_move(self, x, y):
        self.df = self.df.append(
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
        
        self.df = self.df.append(
                {'Device': 'Mouse',
                 'Coordinates': (x,y),
                 'Key': 'n/a',
                 'Event': '{0}'.format(click if pressed else release)
                 }, ignore_index = True)

    # Tracks up/down scrolling
    def on_scroll(self, x, y, dx, dy):
        self.df = self.df.append(
                {'Device': 'Mouse',
                 'Coordinates': (x, y),
                 'Key': 'n/a',
                 'Event': 'Scrolled {0}'.format(
                         'down' if dy < 0 else 'up')
                 }, ignore_index = True)
                 
    # Tracks key presses
    def on_press(self, key):
        self.df = self.df.append(
                {'Device': 'Keyboard',
                 'Coordinates': 'n/a',
                 'Key': key,
                 'Event': 'Pressed key'
                 }, ignore_index = True)

    # Tracks key releases
    def on_release(self, key):
        self.df = self.df.append(
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
        for i, row in self.df.iterrows():
            if row['Device'] == 'Mouse':
                mouse.position = row['Coordinates']
                if row['Event'] == 'Left-clicked':
                    mouse.click(Button.left)
                elif row['Event'] == 'Released left-click':
                    mouse.release(Button.left)
                    time.sleep(10)
                elif row['Event'] == 'Right-clicked':
                    mouse.click(Button.right)
                elif row['Event'] == 'Released right-click':
                    mouse.release(Button.right)
                    time.sleep(10)
                elif row['Event'] == 'Scrolled down':
                    mouse.scroll(0, 1)
                elif row['Event'] == 'Scrolled up':
                    mouse.scroll(0, -1)
            elif row['Device'] == 'Keyboard':
                if row['Event'] == 'Pressed key':
                    kb.press(row['Key'].char)
                elif row['Event'] == 'Released key':
                    kb.release(row['Key'].char)
            else:
                print("TO-DO: Wait...")
                # Extract integer from Event string and wait
                # re.search("\d", row.['Event'])
                # time.sleep(wait)
                    
        print('Finished replay!')
        
    # Print dataframe to the window
    @QtCore.pyqtSlot()
    def printDataTable(self):
        self.setColumnCount(len(self.df.columns))
        self.setRowCount(len(self.df.index))
        
        for i in range(len(self.df.index)):
            for j in range(len(self.df.columns)):
                self.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))
    
    # Insert event below the selected row
    @QtCore.pyqtSlot()
    def on_insert_clicked(self):
        devices = ("Mouse", "Keyboard", "Wait")
        dev, okPressed = QInputDialog.getItem(self, "Inserting action...","Device:", devices, 0, False)
        if okPressed and dev != '':
            print(dev)
        
        if dev == "Mouse":
            coord, okPressed = QInputDialog.getText(self, "Inserting action...","Coordinates:", QLineEdit.Normal, "")
            if okPressed and coord != '':
                print(coord)
            key = "n/a"
            print(key)
            evnts = ("Move", "Left-Clicked", "Released left-click", "Right-Clicked", "Released right-click", "Scrolled up", "Scrolled down")
            ev, okPressed = QInputDialog.getItem(self, "Inserting action...","Event:", evnts, 0, False)
            if okPressed and ev != '':
                print(ev)
        elif dev == "Keyboard":
            coord = "n/a"
            print(coord)
            key, okPressed = QInputDialog.getText(self, "Inserting action...","Key:", QLineEdit.Normal, "")
            if okPressed and key != '':
                print(key)
            evnts = ("Pressed key", "Released key")
            ev, okPressed = QInputDialog.getItem(self, "Inserting action...","Event:", evnts, 0, False)
            if okPressed and ev != '':
                print(ev)
        else:
            coord = "n/a"
            print(coord)
            key = "n/a"
            print(key)
            wait, okPressed = QInputDialog.getInt(self, "Inserting action...","Wait:", 0, 0, 300, 1)
            ev = "Wait for {0} seconds".format(wait)
            if okPressed:
                print(ev)
        
#        newRow = pandas.DataFrame({"Device:": dev, "Coordinates": "(" + coord + ")", "Key": key, "Event": ev}, index=[selectedIndex])
#        self.df = self.df.append(newRow, ignore_index=False, sort=False)
#        self.printDataTable()
        
        self.df.loc[self.currentRow()] = [dev, coord, key, ev]  # adding a row
        self.df.index = self.df.index + 1  # shifting index
        self.df = self.df.sort_index()  # sorting by index
        self.printDataTable()
        
        print('Insert button clicked!')
    
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
        
        # Status Label
        status_label = QtWidgets.QLabel("Click \"Record\" to get started!")

        # Initialize and connect buttons to actions
        record_button = QtWidgets.QPushButton("Record [Ctrl+R]")
        record_button.clicked.connect(table.on_record_clicked)
        
        stop_button = QtWidgets.QPushButton("Stop [Ctrl+Q]")
        stop_button.clicked.connect(table.on_stop_clicked)
        
        play_button = QtWidgets.QPushButton("Play [Ctrl+P]")
        play_button.clicked.connect(table.on_play_clicked)
        
        insert_button = QtWidgets.QPushButton("Insert [Ctrl+I]")
        insert_button.clicked.connect(table.on_insert_clicked)
        
        clear_one_button = QtWidgets.QPushButton("Clear One [Ctrl+O]")
        clear_one_button.clicked.connect(table.on_clear_one_clicked)
        
        clear_all_button = QtWidgets.QPushButton("Clear All [Ctrl+E]")
        clear_all_button.clicked.connect(table.on_clear_all_clicked)
        
        save_button = QtWidgets.QPushButton("Save [Ctrl+S]")
        save_button.clicked.connect(table.on_save_clicked)

        # Set button layout
        button_layout = QtWidgets.QVBoxLayout()
        button_layout.addWidget(status_label, alignment=QtCore.Qt.AlignCenter)
        button_layout.addWidget(record_button, alignment=QtCore.Qt.AlignCenter)
        button_layout.addWidget(stop_button, alignment=QtCore.Qt.AlignCenter)
        button_layout.addWidget(play_button, alignment=QtCore.Qt.AlignCenter)
        button_layout.addWidget(insert_button, alignment=QtCore.Qt.AlignCenter)
        button_layout.addWidget(clear_one_button, alignment=QtCore.Qt.AlignCenter)
        button_layout.addWidget(clear_all_button, alignment=QtCore.Qt.AlignCenter)
        button_layout.addWidget(save_button, alignment=QtCore.Qt.AlignCenter)

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