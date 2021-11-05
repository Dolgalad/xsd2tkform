from xsd_complextype import XSDComplexTypeFrame

from scrollframe import ScrollFrame

from lxml import etree

import tkinter as tk

if __name__=="__main__":
    print("Testing complex types")

    # load the XSD schema
    xsd_schema = etree.parse("spase-2.3.1.xsd")

    # store all simple type definitions
    simple_types = {e.attrib["name"]:e for e in xsd_schema.iter("{*}simpleType")}
    complex_types = {e.attrib["name"]:e for e in xsd_schema.iter("{*}complexType")}

    # create mainwindow and populate
    mainwindow = tk.Tk()
    
    mainframe = tk.Frame(mainwindow)

    scrollFrame = ScrollFrame(mainframe) # add a new scrollable frame.
        
    # populate window with all simpleTypes found in the XSD schema
    c=1
    form_frame = None
    for complex_type in xsd_schema.iter("{*}complexType"):
        form_frame = XSDComplexTypeFrame(parent = scrollFrame.viewPort,\
                element = complex_type,\
                simple_types=simple_types,\
                complex_types=complex_types)
        form_frame.pack(side=tk.TOP, fill=tk.X, expand=True)
        c-=1
        if c==0:
            break
    
    scrollFrame.pack(side="top", fill="both", expand=True)
    
    mainframe.pack(side="top", fill="both", expand=True)
    # add a submit and cancel button at bottom
    action_frame = tk.Frame(scrollFrame.viewPort)
    def save_tree(t):
        with open("mytree.xml","wb") as f:
            a=etree.tostring(t, pretty_print=True)
            f.write(a)
            f.close()
    submit_button = tk.Button(action_frame, text="Submit", command=lambda form=form_frame: save_tree(form.get_content()))
    cancel_button = tk.Button(action_frame, text="Cancel", command=mainwindow.quit)
    submit_button.pack(side=tk.LEFT, fill=tk.X, expand=1)
    cancel_button.pack(side=tk.RIGHT, fill=tk.X, expand=1)
    action_frame.pack(side=tk.TOP, fill=tk.X, expand=1)


    # start event loop
    mainwindow.mainloop()
