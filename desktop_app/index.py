from tkinter import *
from tkinter import ttk


root = Tk() #a new window is defined
root.title("ReFair dekstop app")
root.geometry("600x400") #dimension of the window
#root.geometry("600x400+50+50") changes the point where the window starts. In this case are added 50x and 50y
root.iconbitmap('desktop_app/icons/right_arrow_icon.ico')

root.minsize(400,100)
root.maxsize(1000,1000)

root.mainloop() #needed to render the window. The window is shown thanks to a infinite loop
