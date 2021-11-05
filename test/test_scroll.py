import tkinter as tk
from tkinter import ttk

if __name__=="__main__":
    print("Testing scrollable frame")

    # create mainwindow and populate
    mainwindow = tk.Tk()
    # add a scrollable frame
    from vscrollframe import VerticalScrolledFrame
    frame = VerticalScrolledFrame(mainwindow)
    frame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
    
    print("mainwindow width : {}".format(mainwindow.winfo_width()))
    print("frame width : {}".format(frame.winfo_width()))
    print("frame interior width : {}".format(frame.interior.winfo_width()))

    # populate window with labels
    for i in range(100):
        tk.Label(frame.interior, text=str(i)).pack(side=tk.TOP,\
                fill=tk.Y, expand=True)

    # start event loop
    mainwindow.mainloop()
