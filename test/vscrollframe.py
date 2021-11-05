from tkinter import *   # from x import * is bad practice
from tkinter.ttk import *

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        #vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar = Scrollbar(self)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=TRUE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        #canvas.pack(side=TOP, fill=BOTH, expand=1)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            print("SIZE ", size)
            print("0 0 %s %s" % size)

            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        #def _bound_to_mousewheel(event):
        #    print(event)
        #    canvas.bind_all("<MouseWheel>", _on_mousewheel)   

        #def _unbound_to_mousewheel(event):
        #    print(event)
        #    canvas.unbind_all("<MouseWheel>") 

        def _on_mousewheel(event):
            print(event)
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")  


        #canvas.bind('<Configure>', _configure_canvas)
        #interior.bind('<Enter>', _bound_to_mousewheel)
        ##interior.bind('<Leave>', _unbound_to_mousewheel)
        canvas.bind_all("<MouseWheel>", _on_mousewheel)   

    


if __name__ == "__main__":

    class SampleApp(Tk):
        def __init__(self, *args, **kwargs):
            root = Tk.__init__(self, *args, **kwargs)

            self.frame = VerticalScrolledFrame(root)
            self.frame.pack(fill=BOTH, expand=TRUE)
            
            for i in range(100):
                Label(self.frame.interior, text=str(i)).pack()
            #from spaseeditform import SpaseEditFrame
            #frame = SpaseEditFrame(self.frame.interior, fields=["Name", "Description"], field_types=[Entry, Text])
            #frame.pack(side=TOP, fill=BOTH, expand=TRUE)

    app = SampleApp()
    app.mainloop()

