import tkinter as tk
from tkinter import ttk

from ..core.type import SimpleType, ComplexType

from .simpletype import XSDSimpleTypeFrame
from .complextype import XSDComplexTypeFrame

from .field import XSDInputField

class ChoiceInput(XSDInputField):
    def __init__(self, parent, choice, schema, *args, **kwargs):
        XSDInputField.__init__(self, parent, highlightbackground="green", highlightthickness=2, *args, **kwargs)
        self.schema=schema
        # get the choice types
        self.choice_inputs=[]
        # get the list of choice type
        self.choice_types = [t.type for t in choice.elements]
        self.choice_names = [t.name for t in choice.elements]
        # get occurence bounds for choices
        #choice_occ_bounds = self.get_element_occurence_limits(item)
        choice_occ_bounds = choice.min_occurs, choice.max_occurs
        # set those bounds for all types 
        self.field_counts={}
        self.field_min_counts={}
        self.field_max_counts={}
        for _type in self.choice_types:
            # TODO : check if bounds are correct, if choice type is present somewhere else in the type definition then the bounds are overwritten here, which can be bad
            if _type in self.field_min_counts:
                print("Not good if you see this")
            if _type in self.field_max_counts:
                print("Not good if you see this")
            self.field_min_counts[_type]=choice_occ_bounds[0]
            self.field_max_counts[_type]=choice_occ_bounds[1]
        # frame for storing the selector and choices
        #choice_frame = tk.Frame(self)
        # create a frame to store the choice selector
        #choice_select_frame = tk.Frame(choice_frame)
        choice_select_frame = tk.Frame(self)
        
        # add a choice selector : combobox and button
        #self.choice_type = ttk.Combobox(choice_select_frame, values=self.choice_types, state="readonly")
        self.choice_type = ttk.Combobox(choice_select_frame, values=self.choice_names, state="readonly")

        self.choice_type.current(0)
        from amda_xml_manager import add_image_file
        self.add_img = tk.PhotoImage(file=add_image_file)
        choice_add = tk.Button(choice_select_frame, image=self.add_img, command=lambda: self.add_field())

        self.choice_type.pack(side=tk.LEFT, fill=tk.X, expand=1)
        choice_add.pack(side=tk.RIGHT, expand=0)
        choice_select_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        ##choice_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        #sequence_inputs.append(choice_inputs)
        #return choice_frame
    def has_type(self, t):
        # TODO watch out
        if t in self.choice_names:
            return True
        for _type in self.choice_types:
            if t==_type or t==_type.split(":")[-1]:
                return True
        return False
    def set_content(self, content, update_grid=True):
        # get the name of the item
        ct=content.tag.split("}")[-1]
        
        for c in self.choice_names:
        #for c in self.choice_types:
            ctt=c.split(":")[-1]
            if ct==ctt:
                self.choice_type.set(c)
                self.add_field(content)

        #self.add_field(content)

    def add_field(self, content=None):
        _name = self.choice_type.get()
        #_type = self.choice_type.get()
        _type = self.choice_types[self.choice_names.index(_name)]

        # add the frame
        self.add_frame_by_type(_type, content=content)
    def add_frame_by_type(self, t, content=None):
        # check if the maximum occurences of this field is achieved
        
        if self.field_max_counts[t]=="unbounded":
            pass
            #print("No limit on {} fields".format(t))
        elif t in self.field_counts:
            if self.get_field_count_by_type(t)==self.field_max_counts[t]:
                showerror(title="{} maximum occurences reached".format(t), message="Type {} supports a maximum of {} occurences of type {}".format(self.type, self.field_max_counts[t], t))
                return
        else:
            pass
        
        self.increment_field_count_by_type(t)
                
        f = self.get_frame_by_type(t, parent=self, delete_button=True, content=content)
        f.configure(highlightbackground="blue", highlightthickness=2)
        f.pack(side=tk.TOP, fill=tk.X, expand=1)
        self.choice_inputs.append(f)
        #if container is not None:
        #    container.append(f.winfo_children()[0])
        #self.master.update_grid()

    def get_frame_by_type(self, t, parent=None, delete_button=False, content=None):
        if parent is None:
            parent = self
        
        td=self.schema.get(t)
        nn=self.choice_names[self.choice_types.index(t)]
        print("IN CHOICE type={}, name={}".format(t, nn))
        if isinstance(td, SimpleType):# in self.simple_types:
            return XSDSimpleTypeFrame(t, parent=parent,\
                    name=nn,
                    schema=self.schema,
                    delete_button=delete_button,
                    content=content,
                    widget_config=self.widget_config,
                    on_delete=lambda x=t: self.delete_field(x))
        elif isinstance(td, ComplexType):
            return XSDComplexTypeFrame(t, parent=parent,\
                    name=nn,
                    schema=self.schema,
                    delete_button=delete_button,
                    collapsable=True,
                    content=content,
                    widget_config=self.widget_config,
                    on_delete=lambda x=t: self.delete_field(x))
        else:
            # TODO : add Group support
            print("Group support not yet implemented")
    #def delete_field(self, t, widget):
    #    pass
    def get_field_count_by_type(self, t):
        if t in self.field_counts:
            return self.field_counts[t]
        return 0
    def increment_field_count_by_type(self, t):
        self.field_counts[t]=self.get_field_count_by_type(t)+1
    def decrement_field_count_by_type(self, t):
        self.field_counts[t]=self.get_field_count_by_type(t)-1
 
    def delete_field(self, t, field=None, container=None):
        self.decrement_field_count_by_type(t)
        self.choice_inputs=[w for w in self.choice_inputs if w.winfo_exists()]
        
    def add_content(self, root, content):
        if isinstance(content, list):
            for item in content:
                self.add_content(root, item)
        else:
            if content is not None:
                root.append(content)
    def get_content(self, nsmap=None, qname_attrs=None):
        return [i.get_content(nsmap=nsmap, qname_attrs=qname_attrs) for i in self.choice_inputs]
        #return [i.get_content(i, nsmap=nsmap, qname_attrs=qname_attrs) for i in self.choice_inputs]
