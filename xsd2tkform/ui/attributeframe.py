"""Frame for containing list of attributes
"""

import tkinter as tk
from tkinter import ttk

from .simpletype import XSDAttributeFrame
from .entrywidgets import FloatEntry, IntEntry, BoolEntry
from amda_xml_manager import collapse_image_file, expand_image_file

class AttributeButtonFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        tk.Label(self, text="Add :", anchor=tk.W).grid(row=0, sticky=tk.W)
    def count_visible_children(self):
        c=0
        for child in self.winfo_children():
            ginfo=child.grid_info()
            if "row" in ginfo:
                c+=1
        return c

class AttributeFrame(tk.Frame):
    def __init__(self, parent, attributes=[]):
        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness=1)

        #tk.Label(self, text="Attributes").grid(row=0, columnspan=2, sticky=tk.W)
        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 

        #images
        self.collapse_img = tk.PhotoImage(file=collapse_image_file)
        self.expand_img = tk.PhotoImage(file=expand_image_file)
       
        # add header
        self.get_header_frame()

        # content frame : content that is hidden when collapsed
        self.content_frame = tk.Frame(self)
        self.content_frame.grid_columnconfigure(0, weight=0) 
        self.content_frame.grid_columnconfigure(1, weight=1) 


        self.attributes=attributes
        # attribute counts
        self.counts={a.name:0 for a in self.attributes}

        # button container
        self.button_frame = AttributeButtonFrame(self.content_frame)
        
        self.attribute_inputs=[XSDAttributeFrame(a, parent=self.content_frame,\
                               on_delete=lambda t=a.name: self.delete_attribute(t),\
                               on_add=self.update_grid) for a in self.attributes]

        self.add_attribute_widgets()         

        self.content_frame.grid(row=1, columnspan=2, sticky=tk.EW)
    def set_attribute_content(self, name, value):
        if "}" in name:
            name = name.split("}")[-1]
        print("attrib Setting {} : {}".format(name, value))
        for i in range(len(self.attributes)):
            if name==self.attributes[i].name:
                A=self.attribute_inputs[i]
                A.set(value)

                ginfo=self.attribute_inputs[i].grid_info()
                if not "row" in ginfo:
                    self.attribute_inputs[i].grid()
    def get_attribute_values(self):
        r={}
        for inp in self.attribute_inputs:
            if inp.is_visible():
                v=inp.get()
                if len(v):
                    r[inp.name]=v
        return r
    def add_attribute_widgets(self):
        # add button for each non required attributes
        row,col=0,1
        for att in self.attribute_inputs:
            att.grid(row=row, column=1, sticky=tk.EW)
            l=att.get_label(self.content_frame)
            l.grid(row=row, column=0, sticky=tk.W)
            if not att.mandatory:
                att.grid_remove()
                l.grid_remove()

                b=att.get_add_button(parent=self.button_frame)
                b.grid(row=0, column=col)
            row+=1
            col+=1

    def get_header_frame(self):
        self.header_frame=tk.Frame(self)
        self.header_label=tk.Label(self.header_frame, text="Attributes", anchor=tk.W)
        self.header_label.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.collapse_button=tk.Button(self.header_frame, image=self.collapse_img, command=self.collapse)
        self.collapse_button.pack(side=tk.RIGHT, expand=0)

        self.header_frame.grid(row=0, columnspan=2, sticky=tk.EW)
    def collapse(self):
        self.content_frame.grid_remove()
        #for c in self.winfo_children():
        #    c.grid_remove()
        #self.header_frame.grid()
        self.collapse_button.configure(image=self.expand_img, command=self.expand)
    def expand(self):
        self.content_frame.grid()
        self.collapse_button.configure(image=self.collapse_img, command=self.collapse)
    def delete_attribute(self, name):
        self.counts[name]-=1
        #self.update_grid()
    def update_grid(self):
        row=1
        for f in self.attribute_inputs:
            row+=1
        ttk.Separator(self, orient="horizontal").grid(row=row, columnspan=2, sticky=tk.EW)
        row+=1
        if self.button_frame.count_visible_children()>1:
            self.button_frame.grid(row=row, columnspan=2, sticky=tk.EW)
        else:
            self.button_frame.grid_remove()

    def delete_attribute(self, name):
        self.update_grid()
