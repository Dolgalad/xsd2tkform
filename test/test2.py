import tkinter as tk
from tkinter import ttk

from lxml import etree

class XSDFrame(tk.Frame):
    def __init__(self,parent,  xsd_tree=None,  *args, **kwargs):
        tk.Frame.__init__(self,parent, *args, **kwargs)
        l=tk.Label(self, text="Schema frame").pack()
        self.tree=xsd_tree
        print("SCHEMA TREE : ", xsd_tree, xsd_tree.attrib, xsd_tree.tag)

        self.types={}

        # load types
        self.load_types()

        # now add the widgets for each element that needs filling
        for child in self.tree:
            # ignore comments
            if isinstance(child, etree._Comment):
                continue
            # ignore type definitions
            if child.tag.endswith("Type") or child.tag.endswith("}group"):
                continue
            t=child.tag.split("}")[-1]
            c_type = child.attrib["type"]
            if ":" in c_type:
                c_type = c_type.split(":")[-1]
            print("Child : {}, type: {}".format(t, c_type))
            # add widgets for that type
            f=self.get_type_widget_frame(c_type)
            f.pack()
    def get_type_widget_frame(self, t):
        f=tk.Frame(self)
        tk.Label(f, text="widget frame type : {}".format(t)).pack()
        print("TYPE", self.types[t])
        d = self.types[t]
        for e in d:
            # ignore annotation
            if e.tag.endswith("annotation"):
                continue
            if e.tag.endswith("sequence"):
                seq_frame = SequenceFrame(self, e)
                seq_frame.pack()
                for s_i in e:
                    if s_i.tag.endswith("element"):
                        print("SQEGezq",s_i.tag, s_i.attrib)
                        # create the right widgets for this
                        tk.Label(f, text=s_i.attrib["name"]).pack()
                        tk.Entry(f).pack()
                    elif s_i.tag.endswith("choice"):
                        # add combobox
                        tk.Label(f, text="Choice").pack()
                        cb=ttk.Combobox(f, state="readonly", values=[i.attrib["name"] for i in s_i if "name" in i.attrib])
                        cb.pack()
                        cb.bind("<<ComboboxSelected>>", self.add_type_widgets)
                    else:
                        print("I DONT KNOW")
            if e.tag.endswith("choice"):
                print("choice")
            
        return f
    def add_type_widgets(self, *args):
        print(args)
        tk.Label(self, text="add type widget : {}".format(args)).pack()
    def load_types(self):
        for e in self.tree.iter("{*}simpleType", "{*}complexType", "{*}group"):
            type_name = e.attrib["name"]
            if ":" in type_name:
                type_name=type_name.split(":")[-1]
            self.types[type_name]=e

class XSDForm(tk.Frame):
    def __init__(self, xsd=None, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.tree = etree.parse(xsd)

        # initialize the schema frame
        self.schema_frame = None

        # add combobox for selecting the schema we want
        schema_label = tk.Label(self, text = "Choose schema :")
        schema_label.pack()

        self.schema_selection = ttk.Combobox(self, state="readonly", values=self.get_schema_names())
        self.schema_selection.pack()
        self.schema_selection.bind("<<ComboboxSelected>>", self.schema_selection_callback)
    def get_schema_names(self):
        ans=[]
        c=1
        for e in self.tree.iter(tag="{*}schema"):
            ans.append(str(c))
            c=c+1
        return ans
    def get_schema(self, i):
        c=1
        for e in self.tree.iter(tag="{*}schema"):
            if str(c)==i:
                return e
            else:
                c+=1
        return None

    def schema_selection_callback(self, *args):
        sid=self.schema_selection.get()
        print("Schema selected : {}".format(sid))
        if not self.schema_frame is None:
            self.schema_frame.destroy()
            self.schema_frame=None
        # prepare the frame for editing this schema
        print(self.get_schema(sid))
        self.schema_frame = XSDFrame(self, xsd_tree=self.get_schema(sid))
        self.schema_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

if __name__=="__main__":
    mainwindow = tk.Tk()
    mainwindow.title("XSD form")

    xsd_form = XSDForm(xsd="spase-2.3.1.xsd")
    xsd_form.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    mainwindow.mainloop()
