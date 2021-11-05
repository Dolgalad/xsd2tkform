import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

from lxml import etree

from xsd2tkform.core.type import SimpleType, ComplexType
from xsd2tkform.core.element import Element
from xsd2tkform.core.choice import Choice

from xsd2tkform.ui.simpletype import XSDSimpleTypeFrame
from xsd2tkform.ui.tooltip import ToolTip

from .field import XSDInputField

class XSDComplexTypeFrame(XSDInputField):
    def __init__(self, typename, parent=None, schema=None, delete_button=False, collapsable=False, *args, **kwargs):
        XSDInputField.__init__(self, parent, borderwidth=1,\
                highlightbackground="black",\
                highlightthickness=2,\
                *args, **kwargs)
        # store type of the current field
        self.type = typename
        self.schema = schema

        # store the number of fields of each type, and min and max
        self.field_counts={}
        self.field_min_counts={}
        self.field_max_counts={}
        
        # storage for optional frame
        self.subframes=[]
        
        # frame for containing label, collapse and delete buttons
        lf = tk.Frame(self)
        self.label=tk.Label(lf, text=self.sanitize_type(typename), font="bold")
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=1)


        if delete_button:
            tk.Button(lf, text="X", command=self.delete).pack(side=tk.RIGHT)
        # add a collapse button
        self.collapse_button=None
        if collapsable:
            self.collapse_button = tk.Button(lf, text="_", command=self.collapse)
            self.collapse_button.pack(side=tk.RIGHT)


        lf.pack(side=tk.TOP, fill=tk.X, expand=1)
        
        self.inputs=[] # list of inputs used for constructing the tree
        
        # get type definition
        self.typedef = schema.get(typename)
        if self.typedef is None:
            raise Exception("Typename {} not found".format(typename))
        self.set_tooltip()
        sequence_inputs=[]
        for item in self.typedef.sequence.items:
            if isinstance(item, Element):
                self.set_occurrence_bounds(item)
                element_field = self.get_element_field(item, sequence_inputs)
                element_field.pack(side=tk.TOP, fill=tk.X, expand=1)
            elif isinstance(item, Choice):
                from xsd2tkform.ui.choice import ChoiceInput
                chh = ChoiceInput(self, item, self.schema)
                chh.pack(side=tk.TOP, fill=tk.X, expand=1)
                sequence_inputs.append(chh)
            else:
                # TODO : add groups
                print("Group support not implemeneted yet")
        self.inputs.append(sequence_inputs)
    def collapse(self):
        # hide all inputs
        for i in self.inputs:
            if isinstance(i, list):
                for e in i:
                    e.pack_forget()
            else:
                i.pack_forget()
        # change button action to expand
        self.collapse_button.configure(text="+", command=self.expand)
        # change the label text
        in_val=[]
        for i in self.inputs:
            if isinstance(i, list):
                for e in i:
                    if isinstance(e, XSDSimpleTypeFrame):
                        in_val+=["{}:{}".format(self.sanitize_type(e.type),e.get_value())]
        new_lab = "{}({})".format(self.sanitize_type(self.type),
                ",".join(in_val))
        self.label.configure(text=new_lab)
    def expand(self):
        # hide all inputs
        for i in self.inputs:
            if isinstance(i, list):
                for e in i:
                    e.pack(side=tk.TOP, fill=tk.X, expand=1)
            else:
                i.pack(side=tk.TOP, fill=tk.X, expand=1)
        # change button action to collapse
        self.collapse_button.configure(text="_", command=self.collapse)
        # set original lable
        self.label.configure(text=self.sanitize_type(self.type))
    def delete(self):
        self.master.decrement_field_count_by_type(self.type)
        self.destroy()
    def get_choice_field(self, item, sequence_inputs):
        choice_inputs=[]
        # get the list of choice type
        choice_types = [t.type for t in item.elements]
        # get occurence bounds for choices
        #choice_occ_bounds = self.get_element_occurence_limits(item)
        choice_occ_bounds = item.min_occurs, item.max_occurs
        # set those bounds for all types 
        for _type in choice_types:
            # TODO : check if bounds are correct, if choice type is present somewhere else in the type definition then the bounds are overwritten here, which can be bad
            if _type in self.field_min_counts:
                print("Not good if you see this")
            if _type in self.field_max_counts:
                print("Not good if you see this")
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
        ##choice_frame.pack(side=tk.TOP, fill=tk.X, expand=1)
        sequence_inputs.append(choice_inputs)
        return choice_frame

    def get_element_field(self, item, sequence_inputs):
        if item.min_occurs==0:
            # optional field, add a frame to contain the eventual fields, with a button
            b_frame= tk.Frame(self)
            b=tk.Button(b_frame, text="Add {}".format(item.type), command=lambda t=item.type, frame=b_frame, container=sequence_inputs: self.add_frame_by_type(t, frame, container))
            # add tooltip
            doc_str = self.get_type_docstring(item.type)
            if len(doc_str):
                ttt = ToolTip(b, doc_str)
            b.pack(side=tk.TOP, fill=tk.X, expand=1)

            # temp
            from xsd2tkform.ui.optional import OptionalInput
            bounds=(self.field_min_counts[item.type], self.field_max_counts[item.type])
            of=OptionalInput(self, item, self.schema, bounds=bounds)
            of.pack(side=tk.TOP, fill=tk.X, expand=1)
            sequence_inputs.append(of)
            return of
            return b_frame
        else:
            # mandatory field
            f = self.get_frame_by_type(item.type)
            sequence_inputs.append(f) # store the field for later use
            return f
 
    def set_occurrence_bounds(self, item):
        self.field_min_counts[item.type]=item.min_occurs
        self.field_max_counts[item.type]=item.max_occurs

    def set_tooltip(self):
        if len(self.typedef.annotation.documentation):
            langs = [k for k in self.typedef.annotation.documentation]
            tt = ToolTip(self.label, self.typedef.annotation.documentation[langs[0]])
    
    def get_type_docstring(self, t):
        td=self.schema.get(t)
        a=td.annotation.documentation
        if len(a):
            ls=[l for l in a]
            return td.annotation.documentation[ls[0]]
        return ""
    def get_type_definition(self, t):
        return self.schema.get(t)
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
        print("Current {} field count {}".format(t, self.get_field_count_by_type(t)))
        print([k for k in self.field_counts])
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
        self.master.master.configure(scrollregion=new_scrollregion)


    def add_frame_by_type(self, t, frame=None, container=None):
        print("in add frame by type : " , t)
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
            container.append(f)
            #container.append(f.winfo_children()[0])
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
            from xsd2tkform.ui.choice import ChoiceInput
            if isinstance(obj, list):
                return [self.get_content(i) for i in obj]
            if isinstance(obj, XSDSimpleTypeFrame):
                if obj.winfo_exists():
                    return obj.get_content()
            if isinstance(obj, XSDComplexTypeFrame):
                if obj.winfo_exists():
                    return obj.get_content()
            if isinstance(obj, ChoiceInput):
                if obj.winfo_exists():
                    return obj.get_content()
            from xsd2tkform.ui.optional import OptionalInput
            if isinstance(obj, OptionalInput):
                if obj.winfo_exists():
                    return obj.get_content()

            return

 
        root = etree.Element(self.sanitize_type(self.type))
        # returns tree type
        for c in self.get_content(self.inputs):
            self.add_content(root, c)
        return root

