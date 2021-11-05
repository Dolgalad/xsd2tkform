import tkinter as tk
from tkinter.messagebox import showerror

from xsd2tkform.ui.field import XSDInputField
from xsd2tkform.ui.tooltip import ToolTip

from xsd2tkform.core.type import SimpleType, ComplexType

from xsd2tkform.ui.simpletype import XSDSimpleTypeFrame
from xsd2tkform.ui.complextype import XSDComplexTypeFrame


class OptionalInput(XSDInputField):
    def __init__(self, parent, item, schema, bounds=None, *args, **kwargs):
        XSDInputField.__init__(self, parent , *args, **kwargs)
        self.count=0
        self.bounds=bounds
        self.type = item.type
        self.schema = schema
        self.fields=[]
        b=tk.Button(self, text="Add {}".format(self.sanitize_type(item.type)), command=self.add_field)
        # add tooltip
        doc_str = self.get_type_docstring(item.type)
        if len(doc_str):
            ttt = ToolTip(b, doc_str)
        b.pack(side=tk.TOP, fill=tk.X, expand=1)
    def add_field(self):
        if self.bounds[1]=="unbounded":
            print("No limit on {} fields".format(self.type))
        elif self.count==self.bounds[1]:
            showerror(title="{} maximum occurences reached".format(self.type), message="A maximum of {} occurences of type {}".format(self.bounds[1], self.type))
            return
        else:
            pass
        
        self.count+=1

        f=self.get_frame_by_type(self.type, delete_button=True)
        f.pack(side=tk.TOP, fill=tk.X, expand=1)
        #self.fields.append(f.winfo_children()[0])
        self.fields.append(f)
    def get_frame_by_type(self, t, parent=None, delete_button=False):
        if parent is None:
            parent = self

        td=self.schema.get(t)
        if isinstance(td, SimpleType):# in self.simple_types:
            return XSDSimpleTypeFrame(t, parent=parent,\
                    schema=self.schema,
                    delete_button=delete_button)
        elif isinstance(td, ComplexType):
            return XSDComplexTypeFrame(t, parent=parent,\
                    schema=self.schema,
                    delete_button=delete_button)
        else:
            # TODO : add Group support
            print("Group support not yet implemented")
    def delete_field(self, t, widget):
        print("in delete_field : {}".format(type(widget)))
        print(self.fields)
        widget.destroy()
        self.count-=1
    def get_content(self):
        return [i.get_content() for i in self.fields if i.winfo_exists()]
    def get_type_docstring(self, t):
        td=self.schema.get(t)
        a=td.annotation.documentation
        if len(a):
            ls=[l for l in a]
            return td.annotation.documentation[ls[0]]
        return ""
    def decrement_field_count_by_type(self, t):
        self.count-=1
 

