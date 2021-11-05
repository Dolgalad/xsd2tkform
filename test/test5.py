from tkinter import *
from tkscrolledframe import ScrolledFrame

#from scrollframe import ScrollFrame


# Create a root window
root = Tk()

# Create a ScrolledFrame widget
#sf = ScrollFrame(root)
sf=ScrolledFrame(root)

sf.pack(side="top", expand=1, fill="both")

# Bind the arrow keys and scroll wheel
sf.bind_arrow_keys(root)
sf.bind_scroll_wheel(root)

# Create a frame within the ScrolledFrame
inner_frame = sf.display_widget(Frame)

# Add a bunch of widgets to fill some space
num_rows = 160
num_cols = 1
for row in range(num_rows):
    for column in range(num_cols):
        w=None
        #w = Button(sf.viewPort,
        w = Button(inner_frame,
                  width=15,
                  height=15,
                  borderwidth=2,
                  #relief="groove",
                  #anchor="center",
                  #justify="center",
                  text=str(row * num_cols + column))
        w.config(command=w.destroy)
        w.pack()
        #w.grid(row=row,
        #       column=column,
        #       padx=4,
        #       pady=4)

# Start Tk's event loop
root.mainloop()
