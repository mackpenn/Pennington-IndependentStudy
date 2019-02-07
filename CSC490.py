from tkinter import *
from tkinter import ttk

window = Tk()
window.title("Automation")
frame = Frame(window)
frame.pack()

tree = ttk.Treeview(window)

tree["columns"]=("d","c","e")
tree.column("d", width=100)
tree.column("c", width=100)
tree.column("e", width=100)
tree.heading("d", text="Device")
tree.heading("c", text="Coordinates")
tree.heading("e", text="Event")

## TO-DO: turn this into a loop that will increase the list as recording occurs
tree.insert("", 0, text = "#", values=("mouse/kb", "(x,y)", "left/right"))
            

##def clear():
## TO-DO: create working loop that will clear all table contents
##    for rows in column:
##        tree.delete()
clr = Button(frame, text = "Clear")
    
##def record():
##    TO-DO: implement record functionality from PyAutoGui
rec = Button(frame, text = "Record")

##def save():
##    TO-DO: save table contents in tab-separated file
sv = Button(frame, text = "Save")

tree.pack()
window.mainloop()