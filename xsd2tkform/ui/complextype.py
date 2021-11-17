import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror

from lxml import etree

from ..core.type import SimpleType, ComplexType
from ..core.element import Element, AnyElement
from ..core.choice import Choice

from .simpletype import XSDSimpleTypeFrame, XSDAttributeFrame, XSDAnyInputFrame
from .tooltip import ToolTip

from .field import XSDInputField

from amda_xml_manager import add_image_file, delete_image_file, collapse_image_file, expand_image_file

from .attributeframe import AttributeFrame

class XSDComplexTypeFrame(XSDInputField):
    def __init__(self, typename, parent=None, schema=None, delete_button=False, collapsable=False, filename=None, content=None, name=None, widget_config={}, typedef=None, *args, **kwargs):
        XSDInputField.__init__(self, parent, borderwidth=1,\
                highlightbackground="black",\
                highlightthickness=1,\
                widget_config=widget_config,\
                *args, **kwargs)
        # flag indicating that the fields content has been set
        self.content_has_been_set = False

        self.grid_columnconfigure(0, weight=1) 
        #self.grid_columnconfigure(1, weight=1) 

        # collapsed state
        self.collapsed = False

        # store type of the current field
        self.name = name
        self.type = typename
        self.schema = schema
        
        # keep reference to the label
        self.label=None
        # store the number of fields of each type, and min and max
        self.field_counts={}
        self.field_min_counts={}
        self.field_max_counts={}
        
        # frame for containing label, collapse and delete buttons
        self.header_frame = self.get_header_frame()

        self.delete_img = None
        if delete_button:
            #tk.Button(self.header_frame, text="X", command=self.delete).pack(side=tk.RIGHT)
            self.delete_img = tk.PhotoImage(file=delete_image_file)
            tk.Button(self.header_frame, image=self.delete_img, command=self.delete).pack(side=tk.RIGHT)


        # add a collapse button
        self.expand_img = None
        self.collapse_img = None
        self.collapse_button=None
        if collapsable:
            self.expand_img = tk.PhotoImage(file=expand_image_file)
            self.collapse_img = tk.PhotoImage(file=collapse_image_file)
            #self.collapse_button = tk.Button(self.header_frame, text="_", command=self.collapse)
            self.collapse_button = tk.Button(self.header_frame, image=self.collapse_img, command=self.collapse)
            self.collapse_button.pack(side=tk.RIGHT)

        
        self.inputs=[] # list of inputs used for constructing the tree
        
        # option button frame
        #self.option_button_frame = tk.Frame(self)
        from .buttoncontainer import ButtonContainer
        self.option_button_frame2 = ButtonContainer(self)

        

        #tk.Label(self.option_button_frame, text="Add :").grid(row=0, column=0)
        tk.Label(self.option_button_frame2, text="Add :").grid(row=0, column=0)


        # get type definition
        if typedef is None:
            self.typedef = schema.get(typename)
        else:
            self.typedef = typedef
            #from ..core.element import Element
            if isinstance(typedef, Element):
                if typedef.typedef is not None:
                    self.typedef = typedef.typedef
        if self.typedef is None:
            raise Exception("Typename {} not found".format(typename))

        # attribute container
        if len(self.typedef.attributes):
            self.attribute_frame = AttributeFrame(self, self.typedef.attributes)
            self.attribute_frame.collapse()
        else:
            self.attribute_frame = None
        # field container
        #self.field_frame = tk.Frame(self, highlightbackground="red", highlightthickness=2)
        self.field_frame = tk.Frame(self, highlightbackground=None, highlightthickness=None)
        self.field_frame.grid_columnconfigure(0, weight=0) 
        self.field_frame.grid_columnconfigure(1, weight=1) 



        self.set_tooltip()

        # grid content
        #c=0
        #self.next_row = 1
        option_button_column=1
        # attributes first

        for item in self.typedef.sequence.items:
            #print("item type {} {}".format(type(item), type(item.typedef)))
            if isinstance(item, Element):
                if item.ref is not None:
                    # there can be only ONE
                    refered_element = self.schema.find_ref(item.ref)
                    print("Refered element : {}".format(refered_element))
                    if refered_element.abstract:
                        # find substitutions
                        substitutions = self.schema.find_substitutions(refered_element.name)
                        print("Substitutions : {}".format(substitutions))
                        print("\tnames : {}".format([s.name for s in substitutions]))
                        if len(substitutions)==1:
                            item = substitutions[0]
                        else:
                            #create a choice item
                            item = Choice()
                            for s in substitutions:
                                item.add(s)
                            from .choice import ChoiceInput
                            chh = ChoiceInput(self.field_frame, item, self.schema, widget_config=self.widget_config)
                            #self.grid_contents.append(chh)
                            self.inputs.append(chh)
                            continue

                self.set_occurrence_bounds(item)

                for element_field in self.get_element_field(item, self.inputs):
                    # add to grid contents
                    #self.grid_contents.append(element_field)

                    from .optional import OptionalInput
                    if isinstance(element_field, OptionalInput):
                        # pack the button at the bottom of the field
                        but = element_field.get_add_button(parent = self.option_button_frame2)
                        self.option_button_frame2.add_button(but)
                        but.grid(row=0, column=option_button_column)
                        option_button_column+=1

            elif isinstance(item, Choice):
                from .choice import ChoiceInput
                chh = ChoiceInput(self.field_frame, item, self.schema, widget_config=self.widget_config)
                #self.grid_contents.append(chh)
                self.inputs.append(chh)
            elif isinstance(item, AnyElement):
                from .adaptivetextentry import AdaptiveHeightText
                r=XSDAnyInputFrame(parent=self.field_frame,\
                        input_widget_type=lambda p: AdaptiveHeightText(p, height=3))
                self.inputs.append(r)
 
            else:
                # TODO : add groups
                print("Group support not implemeneted yet")

            #c+=1

        row=1
        if self.attribute_frame is not None:
            self.attribute_frame.grid(row=1, sticky=tk.EW)
            row+=1
        self.field_frame.grid(row=row, sticky=tk.EW)



        # if filename or content was given
        if filename is not None:
            print("Setting content from {}".format(filename))
            self.set_content(filename=filename)
        if content is not None: 
            self.set_content(content=content)

    def get_header_frame(self):
        hf=tk.Frame(self)
        if self.name is None:
            label_text=self.sanitize_type(self.type)
        else:
            label_text=self.name

        #self.header_label=tk.Label(hf, text=label_text, font="bold", anchor="w")
        self.header_label=tk.Label(hf, text=label_text, font=("Helvetica",11,"bold"), anchor="w")

        self.header_label.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.header_label.bind("<Button-1>", self.collapse)
        return hf


    def clear_grid(self):
        for child in self.field_frame.winfo_children():
            # delete labels
            if isinstance(child, tk.Label):
                child.destroy()
            elif isinstance(child, ttk.Separator):
                child.destroy()
            else:
                child.grid_forget()
    def get_label(self, parent):
        print(" ------> ComplexType name={}, type={}".format(self.name, self.type))
        label_text=self.sanitize_type(self.type)
        if isinstance(self.typedef, Element):
            label_text=self.typedef.name
        if self.name is not None:
            label_text=self.name

        self.label = tk.Label(parent, text=label_text+" :")
        self.set_tooltip()
        return self.label
    def get_fields(self):
        from .optional import OptionalInput
        l=[]
        #for item in self.grid_contents:
        for item in self.inputs:
            if isinstance(item, OptionalInput):
                l+=[w for w in item.get_fields()]
            else:
                l.append(item)
        return l
    def remove_separators(self):
        for child in self.field_frame.winfo_children():
            if isinstance(child, ttk.Separator):
                child.destroy()
    def count_grid_contents(self):
        c={}
        for child in self.field_frame.winfo_children():
            if type(child) in c:
                c[type(child)]+=1
            else:
                c[type(child)]=1
        for k in c:
            print("{} : {}".format(k, c[k]))

    def update_attribute_grid(self):
        if self.attribute_frame is not None:
            self.attribute_frame.update_grid()

    def update_grid(self):
        print("update_grid name={}, type={}, self.type={}".format(self.name, self.type, type(self)))
        from .optional import OptionalInput
        from .choice import ChoiceInput
        
        self.remove_separators()
        # attribute grid update
        self.update_attribute_grid()
        # get fields
        new_fields = self.get_fields()
        
        # add the contents of the grid
        self.header_frame.grid(row=0, columnspan=2, sticky=tk.EW)
        if not self.collapsed:
            #ttk.Separator(self, orient="horizontal").grid(row=1, columnspan=2, sticky=tk.EW)
            row=2
            for f in new_fields:
                # add the input field
                grid_info = f.grid_info()
                if "row" in grid_info:
                    if grid_info["row"]!=row:
                        f.grid_forget() # remove the label too
                        f.grid(row=row, column=1, sticky=tk.EW)
                else:
                    f.grid(row=row, column=1, sticky=tk.EW)

                # check the label
                if not isinstance(f, ChoiceInput):
                    if f.label is None:
                        f.get_label(self.field_frame).grid(row=row, column=0, sticky=tk.NW)
                    else:
                        label_grid_info = f.label.grid_info()
                        if "row" in label_grid_info:
                            if label_grid_info["row"]!=row:
                                f.label.grid_forget()
                                f.label.grid(row=row, column=0, sticky=tk.NW)
                        else:
                            f.label.grid(row=row, column=0, sticky=tk.NW)
                row+=1
            ttk.Separator(self.field_frame, orient="horizontal").grid(row=row, columnspan=2, sticky=tk.EW)
            row+=1
            n=len(list(self.option_button_frame2.winfo_children()))
            if n>1:
                self.option_button_frame2.grid(row=row, columnspan=2, sticky=tk.EW)

    def grid(self, *args, **kwargs):
        self.update_grid()
        return super().grid(pady=1,*args, **kwargs)
    def pack(self, *args, **kwargs):
        self.update_grid()
        return super().pack(pady=1, *args, **kwargs)
        if isinstance(self.master, XSDComplexTypeFrame):
            #super().pack(*args, padx=(100,0), **kwargs)
            super().pack(*args, **kwargs)

        else:
            super().pack(*args, **kwargs)
    def iter_inputs(self):
        for e in self.inputs:
            if isinstance(e, list):
                for el in e:
                    yield el
            else:
                yield e
    def set_content(self, filename=None, content=None, update_grid=True):
        if filename is not None:
            root = etree.parse(filename).getroot()
            return self.set_content(content=root, update_grid=update_grid)
        if content is not None:
            # set attribute content
            for att in content.attrib:
                self.attribute_frame.set_attribute_content(att, content.attrib[att])
            # go over children of content
            for child in content:
                if isinstance(child, etree._Comment):
                    continue
                self.set_child_content(child, update_grid=True)
        self.content_has_been_set=True
        if update_grid:
            self.update_grid()
    def is_full(self):
        # check if this field is full : all mandatory fields are filled
        return self.content_has_been_set
    def set_child_content(self, child, update_grid=True):
        ct=child.tag.split("}")[-1]
        ctype = self.schema.get(ct)
        from ..core.element import Element
        for minp in self.iter_inputs():
            if isinstance(minp, XSDSimpleTypeFrame) or isinstance(minp, XSDComplexTypeFrame):
                if minp.name is None:
                    ctt=minp.type.split(":")[-1]
                else:
                    ctt=minp.name
                if ct==ctt:
                    # if the field is already filled skip
                    if minp.is_full():
                        continue
                    minp.set_content(content=child, update_grid=True)
                    if isinstance(minp, XSDComplexTypeFrame):
                        minp.collapse()
                    return
            from .optional import OptionalInput
            if isinstance(minp, OptionalInput):
                if minp.is_full():
                    continue
                ctt=minp.type.split(":")[-1]
                if ct==ctt:
                    minp.set_content(content=child, update_grid=True)
                    return
            from .choice import ChoiceInput
            if isinstance(minp, ChoiceInput):
                if minp.has_type(ct):
                    minp.set_content(content=child, update_grid=True)
                    return

    def collapse(self, event=None):
        self.collapsed = True
        if self.attribute_frame is not None:
            self.attribute_frame.grid_remove()
        for item in self.field_frame.winfo_children():
            if isinstance(item, tk.Label):
                item.grid_remove()
            if isinstance(item, XSDInputField):
                item.grid_remove()
        # collapse the optional button frame
        self.option_button_frame2.grid_remove()

        # change button action to expand
        self.collapse_button.configure(image=self.expand_img, command=self.expand)
        # change the label text
        in_val=[]
        for i in self.inputs:
            if isinstance(i, XSDSimpleTypeFrame):
                tval = str(i.get_value())
                if len(tval)>100:
                    tval=tval[:30]+"..."
                in_val+=["{}:{}".format(self.sanitize_type(i.type),tval)]
        l=self.sanitize_type(self.type)
        if self.name is not None:
            l=self.name
        new_lab = "{}({})".format(l,
                ",".join(in_val))
        w=int(self.winfo_width()*.8)
        self.header_label.configure(text=new_lab, wraplength=w, justify="left")
        self.header_label.bind("<Button-1>", self.expand)
    def expand(self, event=None):
        #self.update_grid()
        from .optional import OptionalInput
        self.collapsed = False
        if self.attribute_frame is not None:
            self.attribute_frame.grid()
        for item in self.field_frame.winfo_children():
            if isinstance(item, tk.Label):
                item.grid()
            if isinstance(item, XSDInputField):
                if isinstance(item, OptionalInput):
                    continue
                item.grid()
                

        # option button frame
        #self.option_button_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=1)
        self.option_button_frame2.grid()

        # change button action to collapse
        self.collapse_button.configure(image=self.collapse_img, command=self.collapse)
        # set original lable
        l=self.sanitize_type(self.type)
        if self.name is not None:
            l=self.name
        self.header_label.configure(text=l, justify="center")
        self.header_label.bind("<Button-1>", self.collapse)
        self.update_grid()

    def delete(self):
        #self.master.decrement_field_count_by_type(self.type)
        self.destroy()
        if self.on_delete is not None:
            self.on_delete()
        if self.label is not None:
            self.label.destroy()
        

    def get_element_field(self, item, sequence_inputs):
        from .optional import OptionalInput
        if isinstance(item, AnyElement):
            of = self.get_frame_by_type(item)
            sequence_inputs.append(of) # store the field for later use
            yield of

        if item.min_occurs==0:
            # temp
            bounds=(self.field_min_counts[item.type], self.field_max_counts[item.type])
            of=OptionalInput(self.field_frame, item, self.schema, bounds=bounds, widget_config=self.widget_config, on_add_field=self.update_grid,\
                    on_delete_field=lambda t=item.type: self.decrement_field_count_by_type(t)\
                    )

            sequence_inputs.append(of)
            yield of
        else:
            # yield mandatory items
            for i in range(item.min_occurs):
                of = self.get_frame_by_type(item)
                if of is None:
                    continue
                sequence_inputs.append(of) # store the field for later use
                yield of
            # get optional bounds
            bounds=[0, self.field_max_counts[item.type]]
            if bounds[1]!="unbounded":
                bounds[1]=bounds[1]-item.min_occurs
            a = (bounds[1]=="unbounded")
            b = False
            if not a:
                b = bounds[1]

            if a or b:
                # yield optional items
                of=OptionalInput(self.field_frame, item, self.schema, bounds=tuple(bounds), widget_config=self.widget_config, on_add_field=self.update_grid, \
                        on_delete_field=lambda t=item.type: self.decrement_field_count_by_type(t)\
                        )
                sequence_inputs.append(of)
                yield of

 
    def set_occurrence_bounds(self, item):
        self.field_min_counts[item.type]=item.min_occurs
        self.field_max_counts[item.type]=item.max_occurs

    def set_tooltip(self):
        if self.label is None or self.typedef is None:
            return
        if self.typedef.annotation is None:
            return
        if len(self.typedef.annotation.documentation):
            langs = [k for k in self.typedef.annotation.documentation]
            tt = ToolTip(self.header_label, self.typedef.annotation.documentation[langs[0]])
    
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


    def get_frame_by_type(self, t, parent=None, delete_button=False):
        #from ..core.type import SimpleType
        if parent is None:
            parent = self.field_frame
        if isinstance(t, AnyElement):
            from .adaptivetextentry import AdaptiveHeightText
            return XSDAnyInputFrame(parent=parent,\
                        input_widget=AdaptiveHeightText)
 

        if t.type is None:
            td=self.schema.get(t.name)
        else:
            td=self.schema.get(t.type)
        if td is None:
            # if type is native type
            if t.type.split(":")[-1]=="string":
                # return a SimpleType object
                from ..core.restriction import Restriction
                #from ..core.type import SimpleType
                td=SimpleType(t.name, restriction=Restriction(base="string"))
                return XSDSimpleTypeFrame(t.name, name=t.name, parent=parent,\
                        schema=self.schema, delete_button=delete_button,\
                        widget_config=self.widget_config,\
                        typedef=td)
 
        if isinstance(td, SimpleType):# in self.simple_types:
            return XSDSimpleTypeFrame(t.type, name=t.name, parent=parent,\
                    schema=self.schema,
                    delete_button=delete_button,
                    widget_config=self.widget_config)
        elif isinstance(td, ComplexType):
            return XSDComplexTypeFrame(t.type, name=t.name, parent=parent,\
                    schema=self.schema,
                    delete_button=delete_button,
                    collapsable=True,
                    widget_config=self.widget_config)
        else:
            # TODO : add Group support
            print("Group support not yet implemented")
            #if td.typedef is None:
            #    return None
            if td.ref is not None:
                return None
            if isinstance(td.typedef, SimpleType):
                return XSDSimpleTypeFrame(t.type, name=t.name, parent=parent,\
                    schema=self.schema,
                    delete_button=delete_button,
                    widget_config=self.widget_config, typedef=td.typedef)

            
            return XSDComplexTypeFrame(td.type, name=td.name, parent=parent,\
                    schema=self.schema,
                    delete_button=delete_button,
                    collapsable=True,
                    widget_config=self.widget_config,
                    typedef=td.typedef)

    def get_value(self):
        return ""
    def add_content(self, root, content):
        if isinstance(content, list):
            for item in content:
                self.add_content(root, item)
        else:
            if content is not None:
                root.append(content)
    def get_attribute_values(self):
        if self.attribute_frame is None:
            return {}
        return self.attribute_frame.get_attribute_values()
    def get_content(self, obj=None, nsmap=None, qname_attrs=None):
        if obj is not None:
            from .choice import ChoiceInput
            if isinstance(obj, list):
                return [self.get_content(i, nsmap=nsmap) for i in obj]
            if isinstance(obj, XSDAnyInputFrame):
                if obj.winfo_exists():
                    return obj.get_content()
            if isinstance(obj, XSDSimpleTypeFrame):
                if obj.winfo_exists():
                    return obj.get_content(nsmap=nsmap)
            if isinstance(obj, XSDComplexTypeFrame):
                if obj.winfo_exists():
                    return obj.get_content(nsmap=nsmap)
            if isinstance(obj, ChoiceInput):
                if obj.winfo_exists():
                    return obj.get_content(nsmap=nsmap)
            from .optional import OptionalInput
            if isinstance(obj, OptionalInput):
                if obj.winfo_exists():
                    return obj.get_content(nsmap=nsmap)

            return

        if nsmap is None:
            root = etree.Element(self.sanitize_type(self.type))
        else:
            root = etree.Element(self.sanitize_type(self.type), qname_attrs, nsmap=nsmap)
        attrib_values=self.get_attribute_values()
        for k in attrib_values:
            root.set(k, attrib_values[k])
        # returns tree type
        for c in self.get_content(self.inputs, nsmap=nsmap):
            if isinstance(c, str):
                root.text=c
                continue
            self.add_content(root, c)
        return root

