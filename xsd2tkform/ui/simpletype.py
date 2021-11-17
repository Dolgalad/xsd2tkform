import tkinter as tk
from tkinter import ttk

from lxml import etree

from .tooltip import ToolTip

from tkcalendar import DateEntry

from .datetime_selector import DatetimeEntry

from .field import XSDInputField

from amda_xml_manager import delete_image_file

from .entrywidgets import IntEntry, FloatEntry, BoolEntry

class XSDAnyInputFrame(XSDInputField):
    def __init__(self, parent, input_widget_type, content=None):
        XSDInputField.__init__(self, parent)

        self.label=None
        self.add_button=None

        self.grid_columnconfigure(0, weight=1) 
        self.input_widget = input_widget_type(self)
        self.input_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.set_content(content)
    def set_content(self, content=None):
        if content is None:
            return
        if isinstance(content, etree._Element):
            self.input_widget.insert(0, etree.tostring(content, pretty_print=True))
            return
        self.input_widget.insert(0, str(content))


    def get_label(self, parent):
        label_text="any :"
        self.label = tk.Label(parent, text=label_text)
        return self.label
    def get_content(self):
        return self.input_widget.get("1.0", tk.END)
 

class XSDAttributeFrame(XSDInputField):
    def __init__(self, attribute, parent, on_delete=None, on_add=None):
        XSDInputField.__init__(self, parent)
        
        self.on_delete=on_delete
        self.on_add=on_add
        self.name = attribute.name
        self.type = attribute.type
        self.attribute = attribute
        if attribute.use=="required":
            self.mandatory = True
        else:
            self.mandatory = False
        self.label=None
        self.add_button=None

        self.grid_columnconfigure(0, weight=1) 
        if self.type.endswith("float"):
            self.input_widget=FloatEntry(self)
        elif self.type.endswith("int") or self.type.endswith("integer"):
            self.input_widget=IntEntry(self)
        elif self.type.endswith("boolean"):
            self.input_widget=BoolEntry(self)
        else:
            self.input_widget=tk.Entry(self)
        self.input_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        if not self.mandatory:
            self.delete_img = tk.PhotoImage(file=delete_image_file)
            #self.db = tk.Button(self, text="X", command=self.delete)
            self.db = tk.Button(self, image=self.delete_img, command=self.delete)
            self.db.pack(side=tk.RIGHT, expand=0)
    def is_visible(self):
        return "row" in self.grid_info()
    def get(self):
        return self.input_widget.get()
    def set(self, value):
        if isinstance(self.input_widget, FloatEntry) or isinstance(self.input_widget, IntEntry) or \
                isinstance(self.input_widget, BoolEntry):
            self.input_widget.set(value)
        else:
            self.input_widget.insert(0, value)
    def get_add_button(self, parent):
        self.add_button = tk.Button(parent, text=self.name, command=self.add)
        return self.add_button
    def add(self):
        # remove the button
        self.grid()
        if self.label is not None:
            self.label.grid()
        if self.add_button is not None:
            self.add_button.grid_remove()
        if self.on_add is not None:
            self.on_add()
    def delete(self, *args):
        self.grid_remove()
        if self.label is not None:
            self.label.grid_remove()
        # replace the add button
        if self.add_button is not None:
            self.add_button.grid()

        if self.on_delete is not None:
            self.on_delete()

    def get_label(self, parent):
        label_text=self.sanitize_type(self.name)
        label_text+=" :"
        self.label = tk.Label(parent, text=label_text)
        return self.label
 
class XSDSimpleTypeFrame(XSDInputField):
    def __init__(self, typename,  parent=None, schema=None, delete_button=False, filename=None, content=None, name=None, widget_config={}, typedef=None, input_widget=None,*args, **kwargs):
        XSDInputField.__init__(self, parent, widget_config=widget_config,\
        #        highlightbackground="blue",\
        #        highlightthickness=1,\
                *args, **kwargs)
        # flag indicating that the content has been set
        self.content_has_been_set = False

        self.grid_columnconfigure(0, weight=1) 
        self.input_widget_type=input_widget

        self.type = typename
        self.name = name

        print("XSDSimpleTypeFrame name={}, type={}".format(self.name, self.type))

        # label reference
        self.label=None

        if typedef is None:
            self.typedef = schema.get(typename)
        else:
            self.typedef = typedef
        
        self.set_tooltip()

        # input widget
        self.input_widget = self.get_input_widget()
        self.input_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # delete button
        self.delete_img = None
        if delete_button:
            self.delete_img = tk.PhotoImage(file=delete_image_file)
            #self.db = tk.Button(self, text="X", command=self.delete)
            self.db = tk.Button(self, image=self.delete_img, command=self.delete)
            self.db.pack(side=tk.RIGHT, expand=0)

        # if a filename was given then load the content
        if filename is not None:
            print("Setting SimpleType content from file : {}".format(filename))
        if content is not None:
            self.set_content(content)
    def get_label(self, parent):
        label_text=self.sanitize_type(self.type)
        if label_text in ["string", "float", "integer"]:
            label_text=self.name

        if self.name is not None:
            label_text=self.name
        else:
            label_text=self.sanitize_type(self.type)
            if label_text in ["string", "float", "integer"]:
                label_text=self.name

        label_text+=" :"
        self.label = tk.Label(parent, text=label_text)
        self.set_tooltip()
        return self.label
    def delete(self):
        # destroy this widget and decrement the field count in
        # the master frame
        #self.master.decrement_field_count_by_type(self.type)
        self.destroy()
        if self.on_delete is not None:
            self.on_delete()
        if self.label is not None:
            self.label.destroy()
    def is_full(self):
        return self.content_has_been_set
    def set_content(self, content, update_grid=True):
        text=content.text
        if text is None:
            text=""
        if isinstance(self.input_widget, ttk.Combobox):
            if not content.text is None:
                self.input_widget.set(content.text)
        elif isinstance(self.input_widget, tk.Text):
            n_lines = len(text.split("\n"))+1
            self.input_widget.insert("1.0", text)
            #self.input_widget.configure(height=n_lines)

        elif isinstance(self.input_widget, tk.Entry):
            self.input_widget.insert(0, text)
        else:
            self.input_widget.set(content.text)
        self.content_has_been_set = True
    def set_tooltip(self):
        if self.label is None:
            return
        if self.typedef is None:
            return
        if self.typedef.annotation is None:
            return
        if len(self.typedef.annotation.documentation):
            langs = [k for k in self.typedef.annotation.documentation]
            tt=ToolTip(self.label, self.typedef.annotation.documentation[langs[0]])
    def get_input_widget(self):
        if self.input_widget_type is not None:
            return self.input_widget_type(self)
        if self.sanitize_type(self.type) in self.widget_config:
            persot = self.widget_config[self.sanitize_type(self.type)]
            if isinstance(persot, tuple):
                return persot[0](self, *persot[1])
            return self.widget_config[self.sanitize_type(self.type)](self)
        if self.typedef.restriction is not None:
            if self.typedef.restriction.base=="xsd:string":
                if len(self.typedef.restriction.enum):
                    #b=ttk.Combobox(self, values=self.typedef.restriction.enum, state="readonly")
                    from .autocompleteentry import AutocompleteCombobox
                    b=AutocompleteCombobox(self)
                    b.set_completion_list(self.typedef.restriction.enum)

                    b.current(0)
                    b.unbind_class("TCombobox","<MouseWheel>")
                    b.unbind_class("TCombobox","<ButtonPress-4>")
                    b.unbind_class("TCombobox","<ButtonPress-5>")

                    return b
                #if "Description" in self.type:
                #    return tk.Text(self)
                return tk.Entry(self)
            if self.typedef.restriction.base=="xsd:dateTime":
                return DatetimeEntry(self)
            if len(self.typedef.restriction.enum):
                return ttk.Combobox(self, values=self.typedef.restriction.enum, state="readonly")
        if self.type.endswith("float"):
            return FloatEntry(self)
        if self.type.endswith("int") or self.type.endswith("integer"):
            return IntEntry(self)
        return tk.Entry(self)
 
    def get_value(self):
        if isinstance(self.input_widget, tk.Text):
            return self.input_widget.get("1.0",tk.END).strip()
        return self.input_widget.get()
    def get_attribute_values(self):
        return {}
    def get_content(self, nsmap=None, qname_attrs=None):
        # returns tree type
        if self.name is None:
            t = self.sanitize_type(self.type)
        else:
            t=self.name
        if nsmap is not None:
            root = etree.Element(t,qname_attrs, nsmap=nsmap)
        else:
            root = etree.Element(t)
        attrib_values=self.get_attribute_values()
        for k in attrib_values:
            root.set(k, attrib_values[k])
        root.text = self.get_value()
        return root



