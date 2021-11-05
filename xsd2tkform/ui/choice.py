import tkinter as tk
from tkinter import ttk

from xsd2tkform.core.type import SimpleType, ComplexType

from xsd2tkform.ui.simpletype import XSDSimpleTypeFrame
from xsd2tkform.ui.complextype import XSDComplexTypeFrame

from xsd2tkform.ui.field import XSDInputField

class ChoiceInput(XSDInputField):
    def __init__(self, parent, choice, schema, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.schema=schema
        # get the choice types
        self.choice_inputs=[]
        # get the list of choice type
        choice_types = [t.type for t in choice.elements]
        # get occurence bounds for choices
        #choice_occ_bounds = self.get_element_occurence_limits(item)
        choice_occ_bounds = choice.min_occurs, choice.max_occurs
        # set those bounds for all types 
        self.field_counts={}
        self.field_min_counts={}
        self.field_max_counts={}
        for _type in choice_types:
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
        self.choice_type = ttk.Combobox(choice_select_frame, values=choice_types, state="readonly")
        self.choice_type.current(0)
        choice_add = tk.Button(choice_select_frame, text="Add", command=lambda: self.add_field())

        self.choice_type.pack(side=tk.LEFT, fill=tk.X, expand=1)
        choice_add.pack(side=tk.RIGHT, expand=0)
        choice_select_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        ##choice_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        #sequence_inputs.append(choice_inputs)
        #return choice_frame
    def add_field(self):
        _type = self.choice_type.get()

        # add the frame
        self.add_frame_by_type(_type)
    def add_frame_by_type(self, t):
        # check if the maximum occurences of this field is achieved
        
        if self.field_max_counts[t]=="unbounded":
            print("No limit on {} fields".format(t))
        elif t in self.field_counts:
            if self.get_field_count_by_type(t)==self.field_max_counts[t]:
                showerror(title="{} maximum occurences reached".format(t), message="Type {} supports a maximum of {} occurences of type {}".format(self.type, self.field_max_counts[t], t))
                return
        else:
            pass
        
        self.increment_field_count_by_type(t)
                
        f = self.get_frame_by_type(t, parent=self, delete_button=True)
        f.pack(side=tk.TOP, fill=tk.X, expand=1)
        #self.choice_inputs.append(f.winfo_children()[0])
        print("in choice_input append : {}".format(type(f)))
        self.choice_inputs.append(f)
        #if container is not None:
        #    container.append(f.winfo_children()[0])
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
                    delete_button=delete_button,
                    collapsable=True)
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
 
    def delete_field(self, t, field, container=None):
        field_dims = (field.winfo_width(), field.winfo_height())
        field.destroy()
        self.decrement_field_count_by_type(t)
        current_scroll_region=self.master.master.bbox("all")
        new_scrollregion= (current_scroll_region[0],
                current_scroll_region[1],
                current_scroll_region[2]-field_dims[0],
                current_scroll_region[3]-field_dims[1])

        # WORKS
        self.master.master.master.configure(scrollregion=new_scrollregion)


    def add_content(self, root, content):
        if isinstance(content, list):
            for item in content:
                self.add_content(root, item)
        else:
            if content is not None:
                root.append(content)
    def get_content(self):
        return [i.get_content(i) for i in self.choice_inputs]
