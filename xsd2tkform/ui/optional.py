import tkinter as tk
from tkinter.messagebox import showerror

from .field import XSDInputField
from .tooltip import ToolTip

from ..core.type import SimpleType, ComplexType

from .simpletype import XSDSimpleTypeFrame
from .complextype import XSDComplexTypeFrame


class OptionalInput(XSDInputField):
    def __init__(self, parent, item, schema, bounds=None, on_add_field=None, on_delete_field=None, *args, **kwargs):
        XSDInputField.__init__(self, parent , \
                highlightbackground="red",\
                highlightthickness=1,\

                *args, **kwargs)
        self.grid_columnconfigure(0, weight=1) 
        self.count=0
        self.bounds=bounds
        self.type = item.type
        self.item=item
        self.schema = schema

        self.fields=[]
        self.add_button2=None
        self.next_row=0
        self.label_frame=None
        self.label=None

        self.on_add_field=on_add_field
        self.on_delete_field=on_delete_field
    def is_full(self):
        return self.count == self.bounds[1]
    def remove_label(self):
        if self.label is not None:
            self.label.destroy()
            self.label=None

    def set_label_frame(self, frame):
        self.label_frame=frame
        
    def get_add_button(self, parent):
        button_text=self.sanitize_type(self.type)
        if button_text in ["float", "string", "integer", "?"]:
            button_text=self.item.name
        self.add_button2= tk.Button(parent, text=button_text, command=self.add_field)
        doc_str = self.get_type_docstring(self.type)
        if len(doc_str):
            ttt = ToolTip(self.add_button2, doc_str)


        return self.add_button2
    def set_content(self, content, update_grid=True):
        self.add_field(content=content, update_grid=update_grid)
    def add_label(self):
        if self.label_frame is not None and self.label is None:
            self.label=tk.Label(self.label_frame, text=self.sanitize_type(self.type)+":")
            self.label.grid()
    def get_fields(self):
        self.fields = [w for w in self.fields if w.winfo_exists()]
        return self.fields
    def add_field(self, content=None, update_grid=True):
        if self.bounds[1]=="unbounded":
            pass
        elif self.count==self.bounds[1]:
            showerror(title="{} maximum occurences reached".format(self.type), message="A maximum of {} occurences of type {}".format(self.bounds[1], self.type))
            return
        else:
            pass
        self.add_label()
        self.count+=1
        
        if self.count <= self.bounds[0]:
            f=self.get_frame_by_type(self.type, delete_button=False, content=content, parent=self.master, update_grid=update_grid)
        else:
            f=self.get_frame_by_type(self.type, delete_button=True, content=content, parent=self.master, update_grid=update_grid)
        if f is None:
            return 
        self.fields.append(f)
        if isinstance(f, XSDComplexTypeFrame):
            f.collapse()


        # if the maximum number of fields of this type is attained then remove the add button
        if self.count == self.bounds[1] and self.add_button2 is not None:
            self.add_button2.grid_remove()

        # update grid in parent
        if content is None:
            if self.on_add_field is not None:
                self.on_add_field()
            #self.master.update_grid()

    def get_frame_by_type(self, t, parent=None, delete_button=False, content=None, update_grid=True):
        if parent is None:
            parent = self

        td=self.schema.get(t)
        if td is None:
            # if type is native type
            ttt=t.split(":")[-1]
            if ttt=="string" or ttt=="float" or ttt=="integer" or ttt=="int":
                # return a SimpleType object
                from ..core.restriction import Restriction
                #from ..core.type import SimpleType
                td=SimpleType(self.item.name, restriction=Restriction(base="string"))
                #return XSDSimpleTypeFrame(self.item.name, name=self.item.name, parent=parent,\
                return XSDSimpleTypeFrame(ttt, name=self.item.name, parent=parent,\
                        schema=self.schema, delete_button=delete_button,\
                        widget_config=self.widget_config,\
                        typedef=td,\
                        on_delete=self.delete_field)
        

        if isinstance(td, SimpleType):# in self.simple_types:
            return XSDSimpleTypeFrame(t, parent=parent,\
                    schema=self.schema,
                    delete_button=delete_button,
                    content=content,
                    widget_config=self.widget_config, 
                    on_delete=self.delete_field)
        elif isinstance(td, ComplexType):
            return XSDComplexTypeFrame(t, parent=parent,\
                    schema=self.schema,
                    delete_button=delete_button,
                    content=content,
                    collapsable=True,
                    widget_config=self.widget_config,
                    on_delete=self.delete_field)
        else:
            # TODO : add Group support
            print("Group support not yet implemented")
    def delete_field(self, t=None, widget=None):
        # doesn't seem to be used
        self.fields = [w for w in self.fields if w.winfo_exists()]
        self.decrement_field_count_by_type(self.type)
        #self.count-=1

        if self.bounds[1]!="unbounded":
            if self.bounds[1]-self.count == 1:
                #self.add_button2.pack(side=tk.LEFT)
                self.add_button2.grid()
        if self.on_delete_field is not None:
            self.on_delete_field()
        #self.master.update_grid()
    def get_content(self, nsmap=None, qname_attrs=None):
        return [i.get_content(nsmap=nsmap, qname_attrs=qname_attrs) for i in self.fields if i.winfo_exists()]
    def get_type_docstring(self, t):
        if t is None:
            return ""
        td=self.schema.get(t)
        if td is None or (not hasattr(td, "annotation")):
            return ""
        a=td.annotation.documentation
        if len(a):
            ls=[l for l in a]
            return td.annotation.documentation[ls[0]]
        return ""
    def decrement_field_count_by_type(self, t, widget=None):
        self.count-=1

