"""XSDFormFactory definition
"""
import tkinter as tk

from xsd2tkform.form import XSDForm
from xsd2tkform.core.parser import XSDParser
from xsd2tkform.core.type import SimpleType, ComplexType

from xsd2tkform.ui.simpletype import XSDSimpleTypeFrame
from xsd2tkform.ui.complextype import XSDComplexTypeFrame
from xsd2tkform.ui.scrollframe import ScrollFrame
class XSDFormFactory:
    def __init__(self, parser=None):
        self.parser = parser

    def get_form(self, typename, parent):
        if not typename in self.parser.schemas[0]:
            raise Exception("Type {} not found")
        typedef = self.parser.get(typename)
        if isinstance(typedef, SimpleType):
            return XSDSimpleTypeFrame(typename, schema=self.parser.schemas[0], parent=parent, delete_button=False)
        if isinstance(typedef, ComplexType):
            return XSDComplexTypeFrame(typename, schema=self.parser.schemas[0], parent=parent, delete_button=False)


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
    print("Creating form for type : {}".format(typenames[0]))
    print(typenames)


    # form factory
    factory=XSDFormFactory(parser)
    
    app = ExampleApp()
    mainframe = tk.Frame(app)
    scrollframe = ScrollFrame(mainframe) # add a new scrollable frame.
        
    # populate window with all simpleTypes found in the XSD schema
    #for t in typenames:
    form_frame = factory.get_form(typename = typenames[0], parent = scrollframe.viewPort)
    form_frame.pack(side=tk.TOP, fill=tk.X, expand=1)

    # add a submit and cancel button
    def save_form():
        tree = etree.ElementTree(form_frame.get_content())
        from tkinter.filedialog import askopenfilename
        filename = askopenfilename()
        tree.write(filename, pretty_print=True)
    submit_button = tk.Button(scrollframe.viewPort, text="Submit", command=save_form)
    cancel_button = tk.Button(scrollframe.viewPort, text="Cancel", command=app.quit)
    submit_button.pack(side=tk.LEFT, fill=tk.X, expand=1)
    cancel_button.pack(side=tk.RIGHT, fill=tk.X, expand=1)
    
    scrollframe.pack(side="top", fill="both", expand=True)
    mainframe.pack(side="top", fill="both", expand=True)

    app.mainloop()


