import tkinter as tk
from tkinter import ttk

from lxml import etree

from tooltip import ToolTip

from tkcalendar import DateEntry

from datetime_selector import DatetimeEntry

class XSDSimpleTypeFrame(tk.Frame):
    def __init__(self, parent=None, element=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.type = self.get_element_type(element)
        if element is not None:
            # add label with name
            self.label = tk.Label(self, text="{}: ".format(element.attrib["name"]))
            #self.label.grid(row=0,column=0)
            self.label.pack(side=tk.LEFT, expand=0)
            # iterate over type definition elements and populate the frame
            for el in element:
                # ignore annotation
                if el.tag.endswith("annotation"):
                    # add tool tip
                    if el[0].tag.endswith("documentation"):
                        if el[0].text is not None:
                            tt=ToolTip(self.label, el[0].text)
                    continue
                if el.tag.endswith("list"):
                    self.input_widget = tk.Entry(self)
                    #self.input_widget.grid(row=0, column=1)
                    #self.input_widget.pack(side=tk.RIGHT, fill=tk.X, expand=1)
                elif el.tag.endswith("restriction"):

                    # get the type of Entry
                    if len(el)==0:
                        # check the type
                        input_type = el.attrib["base"]
                        if input_type == "xsd:dateTime":
                            #self.input_widget = DateEntry(self)
                            self.input_widget = DatetimeEntry(self)
                        else:
                            # only a type restriction, add an entry widget
                            self.input_widget = tk.Entry(self)
                    
                    else:
                        # enumerate options
                        vals = []
                        for item in el.iter("{*}enumeration"):
                            vals.append(item.attrib["value"])
                        if len(vals):
                            self.input_widget = ttk.Combobox(self, state="readonly", values=vals)
                            self.input_widget.current(0)
                            #self.input_widget.grid(row=0,column=1)
                        else:
                            # no enumeration found add a simple entry
                            self.input_widget=tk.Entry(self)
                            #self.input_widget.grid(row=0, column=1)
                else:
                    pass
                #self.input_widget.grid(row=0, column=1)
                self.input_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    def get_element_type(self, element, attrib_tag="name"):
        t=element.attrib[attrib_tag]
        if ":" in t:
            return t.split(":")[-1]
        return t
 
    def get_value(self):
        return self.input_widget.get()
    def get_content(self):
        # returns tree type
        root = etree.Element(self.type)
        root.text = self.get_value()
        return root



