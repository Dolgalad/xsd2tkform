import tkinter as tk
from tkinter import ttk

from lxml import etree

from xsd2tkform.ui.tooltip import ToolTip

from tkcalendar import DateEntry

from xsd2tkform.ui.datetime_selector import DatetimeEntry

from .field import XSDInputField
class XSDSimpleTypeFrame(XSDInputField):
    def __init__(self, typename,  parent=None, schema=None, delete_button=False, *args, **kwargs):
        XSDInputField.__init__(self, parent, *args, **kwargs)

        self.type = typename
        self.label = tk.Label(self, text="{}: ".format(self.sanitize_type(typename)))
        self.label.pack(side=tk.LEFT, expand=0)

        self.typedef = schema.get(typename)
        
        self.set_tooltip()

        # input widget
        self.input_widget = self.get_input_widget()
        self.input_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # delete button
        if delete_button:
            self.db = tk.Button(self, text="X", command=self.delete)
            self.db.pack(side=tk.RIGHT, expand=0)
    def delete(self):
        # destroy this widget and decrement the field count in
        # the master frame
        print("self id : ", id(self))
        print([id(e) for e in self.master.fields])
        print(self.master.fields)
        self.master.decrement_field_count_by_type(self.type)
        self.destroy()
    def set_tooltip(self):
        if len(self.typedef.annotation.documentation):
            langs = [k for k in self.typedef.annotation.documentation]
            tt = ToolTip(self.label, self.typedef.annotation.documentation[langs[0]])
    def get_input_widget(self):
        if self.typedef.restriction is not None:
            if self.typedef.restriction.base=="xsd:string":
                if len(self.typedef.restriction.enum):
                    b=ttk.Combobox(self, values=self.typedef.restriction.enum, state="readonly")
                    b.current(0)
                    return b
                return tk.Entry(self)
            if self.typedef.restriction.base=="xsd:dateTime":
                return DatetimeEntry(self)
            if len(self.typedef.restriction.enum):
                return ttk.Combobox(self, values=self.typedef.restriction.enum, state="readonly")
        return tk.Entry(self)
 
    def get_value(self):
        return self.input_widget.get()
    def get_content(self):
        # returns tree type
        t = self.sanitize_type(self.type)
        root = etree.Element(t)
        root.text = self.get_value()
        return root



