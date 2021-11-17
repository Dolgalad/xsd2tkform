"""XSDFormFactory definition
"""
import tkinter as tk

from .form import XSDForm
from .core.parser import XSDParser
from .core.type import SimpleType, ComplexType

from .ui.simpletype import XSDSimpleTypeFrame
from .ui.complextype import XSDComplexTypeFrame
from .ui.scrollframe import ScrollFrame
class XSDFormFactory:
    def __init__(self, parser=None, widget_config={}):
        self.widget_config = widget_config
        self.parser = parser
    def get_schema_form(self, parent):
        # get form for schema
        schema = self.parser.schemas[0]
        root_frame = tk.Frame(parent)
        for item in schema.root_items:
            item_form = self.get_form(item.name, parent=root_frame)
            item_form.pack(side=tk.TOP, fill=tk.X, expand=1)
        return root_frame
    def get_form(self, typename, parent, filename=None):
        if not typename in self.parser.schemas[0]:
            raise Exception("Type '{}' not found".format(typename))
        typedef = self.parser.get(typename)
        if isinstance(typedef, SimpleType):
            return XSDSimpleTypeFrame(typename, schema=self.parser.schemas[0], parent=parent, delete_button=False, filename=filename, widget_config=self.widget_config)
        if isinstance(typedef, ComplexType):
            return XSDComplexTypeFrame(typename, schema=self.parser.schemas[0], parent=parent, delete_button=False, filename=filename, widget_config=self.widget_config)
        from .core.element import Element
        if isinstance(typedef, Element):
            if typedef.typedef is None:
                return self.get_form(typedef.type, parent=parent, filename=filename)
            if isinstance(typedef.typedef, ComplexType):
                return XSDComplexTypeFrame(typedef.name, schema=self.parser.schemas[0], parent=parent, delete_button=False, filename=filename, widget_config=self.widget_config, typedef=typedef)
            if isinstance(typedef.typedef, SimpleType):
                return XSDSimpleTypeFrame(typedef.name, schema=self.parser.schemas[0], parent=parent, delete_button=False, filename=filename, widget_config=self.widget_config, typedef=typedef.typedef)


# example app
class ExampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("XSDFormFactory example")


if __name__=="__main__":
    import sys
    from lxml import etree
    if len(sys.argv)<2:
        print("Missing XSD file. Exiting")
        exit(0)
    xsd_filename=sys.argv[1]

    # parse the input 
    parser = XSDParser(xsd_filename)
    # list complex types
    typenames = [k for k in parser.schemas[0].complex_types]
    print("Simple types : \n", [k for k in parser.schemas[0].simple_types])
    print("Complex types : \n", [k for k in parser.schemas[0].complex_types])
    print("Elements : \n", [e.type for e in parser.schemas[0].items])
    print("Root elements : \n", parser.schemas[0].root_items)
    print("Creating form for type : {}".format(typenames[0]))
    print()
    for e in parser.schemas[0].items:
        if e.type=="get":
            print(e)
    print()
    print(parser.schemas[0].complex_types["GetterType"])
    #exit()

    # form factory
    factory=XSDFormFactory(parser)
    
    
    app = ExampleApp()
    mainframe = tk.Frame(app)
    scrollframe = ScrollFrame(mainframe) # add a new scrollable frame.
        
    # populate window with all simpleTypes found in the XSD schema
    #form_frame = factory.get_schema_form(parent = scrollframe.viewPort)
    #form_frame.pack(side=tk.TOP, fill=tk.X, expand=1)

    tk.Label(scrollframe.viewPort, text="FILLED").pack(side=tk.TOP, fill=tk.X, expand=1)

    filled_form = factory.get_form("param", parent=scrollframe.viewPort, filename="ace_r.xml")
    filled_form.pack(side=tk.TOP, fill=tk.X, expand=1)
    #for t in typenames:
    #    #form_frame = factory.get_form(typename = t, parent = scrollframe.viewPort)
    #    form_frame = factory.get_schema_form(parent = scrollframe.viewPort)
    #    form_frame.pack(side=tk.TOP, fill=tk.X, expand=1)

    # add a submit and cancel button
    def save_form():
        tree = etree.ElementTree(filled_form.get_content())
        from tkinter.filedialog import askopenfilename
        filename = askopenfilename()
        tree.write(filename, pretty_print=True, xml_declaration=True, encoding="utf-8")
    submit_button = tk.Button(scrollframe.viewPort, text="Submit", command=save_form)
    cancel_button = tk.Button(scrollframe.viewPort, text="Cancel", command=app.quit)
    submit_button.pack(side=tk.LEFT, fill=tk.X, expand=1)
    cancel_button.pack(side=tk.RIGHT, fill=tk.X, expand=1)
    
    scrollframe.pack(side="top", fill="both", expand=True)
    mainframe.pack(side="top", fill="both", expand=True)

    app.mainloop()


