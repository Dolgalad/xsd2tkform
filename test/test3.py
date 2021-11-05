#from xsd_simple_type import XSDSimpleTypeFrame
import tkinter as tk
from tkinter import ttk

from lxml import etree

from xsd_simpletype import XSDSimpleTypeFrame

if __name__=="__main__":
    print("Testing simple type forms")

    # load the XSD schema
    xsd_schema = etree.parse("spase-2.3.1.xsd")

    # create mainwindow and populate
    mainwindow = tk.Tk()
    # add a scrollable frame
    from vscrollframe import VerticalScrolledFrame
    frame = VerticalScrolledFrame(mainwindow)
    frame.pack(fill=tk.BOTH, expand=tk.TRUE)
    
    # configure grid layout for frame interior
    frame.interior.columnconfigure(0, weight=1)
    frame.interior.columnconfigure(1, weight=1)



    # populate window with all simpleTypes found in the XSD schema
    for simple_type in xsd_schema.iter("{*}simpleType"):
        f = XSDSimpleTypeFrame(parent = frame.interior, element = simple_type)
        f.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # start event loop
    mainwindow.mainloop()
