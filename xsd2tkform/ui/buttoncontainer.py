"""Frame for containing optional field buttons
"""
import tkinter as tk

class ButtonContainer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        #tk.Frame.__init__(self, parent, highlightbackground="magenta", highlightthickness=3, *args, **kwargs)
        tk.Frame.__init__(self, parent, highlightbackground=None, highlightthickness=None, *args, **kwargs)

        self.buttons = []
        
        self.bind("<Configure>", self.update_layout)
    def add_button(self, button):
        self.buttons.append(button)
    def update_layout(self, event):
        pass
        #print("Update layout {}".format(event))



