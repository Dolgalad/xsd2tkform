import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

from lxml import etree

from xsd_simpletype import XSDSimpleTypeFrame
from tooltip import ToolTip

class XSDComplexTypeFrame(tk.Frame):
    def __init__(self, parent=None, element=None, simple_types=None, complex_types=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, borderwidth=1,\
                highlightbackground="black",\
                highlightthickness=1,\
                *args, **kwargs)
        # store type of the current field
        self.type = element.attrib["name"]
        self.simple_types=simple_types
        self.complex_types=complex_types

        # store the number of fields of each type, and min and max
        self.field_counts={}
        self.field_min_counts={}
        self.field_max_counts={}
        
        # storage for optional frame
        self.subframes=[]

        self.label=tk.Label(self, text=element.attrib["name"])
        self.label.pack()
        
        self.inputs=[] # list of inputs used for constructing the tree

        # print children
        for child in element:
            # ignore annotations
            if child.tag.endswith("annotation"):
                # add tooltip
                if child[0].text is not None:
                    # add tool tip
                    tt = ToolTip(self.label, child[0].text)
                
            # sequence
            if child.tag.endswith("sequence"):
                sequence_inputs = []
                # print elements in the sequence
                for item in child:
                    if item.tag.endswith("element"):
                        t = self.get_element_type(item)
 
                        # check if item is mandatory or not
                        (min_oc, max_oc)=self.get_element_occurence_limits(item)
                        self.field_min_counts[t]=min_oc
                        self.field_max_counts[t]=max_oc
                        
                        if min_oc==0:
                            # optional field, add a frame to contain the eventual fields, with a button
                            b_frame= tk.Frame(self)
                            b=tk.Button(b_frame, text="Add {}".format(t), command=lambda t=t, frame=b_frame, container=sequence_inputs: self.add_frame_by_type(t, frame, container))
                            # add tooltip
                            doc_str = self.get_type_docstring(t)
                            if len(doc_str):
                                ttt = ToolTip(b, doc_str)
                            b.pack(side=tk.TOP, fill=tk.X, expand=1)
                            b_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
                        else:
                            # mandatory field
                            f = self.get_frame_by_type(t)
                            sequence_inputs.append(f) # store the field for later use
                            f.pack(side=tk.TOP, fill=tk.X, expand=1)
 
                    if item.tag.endswith("choice"):
                        choice_inputs=[]
                        # get the list of choice type
                        choice_types = self.get_choice_types(item)
                        # get occurence bounds for choices
                        choice_occ_bounds = self.get_element_occurence_limits(item)
                        # set those bounds for all types 
                        for _type in choice_types:
                            # TODO : check if bounds are correct, if choice type is present somewhere else in the type definition then the bounds are overwritten here, which can be bad
                            if _type in self.field_min_counts:
                                print("AAAAAAAAAAAa")
                            if _type in self.field_max_counts:
                                print("BBBBBBBBBBBBBb")
                            self.field_min_counts[_type]=choice_occ_bounds[0]
                            self.field_max_counts[_type]=choice_occ_bounds[1]
                        # frame for storing the selector and choices
                        choice_frame = tk.Frame(self)
                        # create a frame to store the choice selector
                        choice_select_frame = tk.Frame(choice_frame)
                        
                        # add a choice selector : combobox and button
                        choice_type = ttk.Combobox(choice_select_frame, values=choice_types, state="readonly")
                        choice_type.current(0)
                        choice_add = tk.Button(choice_select_frame, text="Add", command=lambda w=choice_type, frame=choice_frame, container=choice_inputs: self.add_frame_by_type(w.get(), frame, container))

                        choice_type.pack(side=tk.LEFT, fill=tk.X, expand=1)
                        choice_add.pack(side=tk.RIGHT, expand=0)
                        choice_select_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
                        choice_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
                        sequence_inputs.append(choice_inputs)
                self.inputs.append(sequence_inputs)
    def get_type_docstring(self, t):
        tree=self.get_type_definition(t)
        for e in tree.iter("{*}documentation"):
            return e.text
        return ""
    def get_type_definition(self, t):
        if t in self.simple_types:
            return self.simple_types[t]
        return self.complex_types[t]
    def get_choice_types(self, element):
        ans=[]
        for child in element:
            if child.tag.endswith("element"):
                ans.append(self.get_element_type(child))
        return ans
    def get_element_occurence_limits(self, element):
        min_oc = int(element.attrib["minOccurs"])
        if "maxOccurs" in element.attrib:
            max_oc=element.attrib["maxOccurs"]
            if max_oc.isdigit():
                max_oc=int(max_oc)
        else:
            max_oc=None
        return min_oc, max_oc

    def get_element_type(self, element):
        t=element.attrib["type"]
        if ":" in t:
            return t.split(":")[-1]
        return t
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
        print(self.winfo_width(), self.winfo_height())
        print(self.master, type(self.master))
        print("master id : ", id(self.master))
        #self.master.master.master.onFrameConfigure(None)
        #self.master.master.event_generate("<Configure>", x=1, y=4, width=600, height=108)
        #self.master.event_generate("<Configure>", x=1, y=4, width=600, height=108)
        current_scroll_region=self.master.master.bbox("all")
        print("current scrollregion : {}".format(current_scroll_region))
        print("field dims ", field_dims)
        new_scrollregion= (current_scroll_region[0],
                current_scroll_region[1],
                current_scroll_region[2]-field_dims[0],
                current_scroll_region[3]-field_dims[1])

        #print("field dimensions : {}".format((field.winfo_width(), field.winfo_height())))
        # WORKS
        #self.master.master.configure(scrollregion=(4,4,604,112))
        self.master.master.configure(scrollregion=new_scrollregion)


    def add_frame_by_type(self, t, frame=None, container=None):
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
                
        if frame is None:
            f = self.get_frame_by_type(t, delete_button=True)
            f.pack(side=tk.TOP, fill=tk.X, expand=1)
        else:
            f = self.get_frame_by_type(t, parent=frame, delete_button=True)
            f.pack(side=tk.TOP, fill=tk.X, expand=1)
        if container is not None:
            container.append(f.winfo_children()[0])
    def get_frame_by_type(self, t, parent=None, delete_button=False):
        if parent is None:
            parent = self
        if delete_button:
            # create a frame to hold the fiel and the delete button
            tf=tk.Frame(parent)
            # add the fields without button
            fields=self.get_frame_by_type(t, tf)
            fields.pack(side=tk.LEFT, fill=tk.X, expand=True)
            # button
            del_button = tk.Button(tf, text="Delete", command=lambda t=t, widget=tf: self.delete_field(t, widget))
            del_button.pack(side=tk.RIGHT, expand=False)
            return tf

        if t in self.simple_types:
            return XSDSimpleTypeFrame(parent=parent,\
                    element=self.simple_types[t])
        else:
            return XSDComplexTypeFrame(parent=parent,\
                    simple_types=self.simple_types,\
                    complex_types=self.complex_types,\
                    element=self.complex_types[t])
    def get_value(self):
        return ""
    def add_content(self, root, content):
        if isinstance(content, list):
            for item in content:
                self.add_content(root, item)
        else:
            if content is not None:
                root.append(content)
    def get_content(self, obj=None):
        if obj is not None:
            if isinstance(obj, list):
                return [self.get_content(i) for i in obj]
            if isinstance(obj, XSDSimpleTypeFrame):
                if obj.winfo_exists():
                    return obj.get_content()
            if isinstance(obj, XSDComplexTypeFrame):
                if obj.winfo_exists():
                    return obj.get_content()
            return
        root = etree.Element(self.type)
        # returns tree type
        for c in self.get_content(self.inputs):
            self.add_content(root, c)
        def inlen(i):
            c=0
            for item in i:
                if isinstance(item, list):
                    c+=inlen(item)
                else:
                    c+=1
            return c
        return root

