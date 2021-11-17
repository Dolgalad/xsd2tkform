"""Base XSD input field definition
"""
import tkinter as tk


class XSDInputField(tk.Frame):
    def __init__(self, parent, content=None, widget_config={}, on_delete=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.widget_config=widget_config
        self.on_delete = on_delete
        if content is not None:
            self.set_content(content)
    def sanitize_type(self, t):
        if t is None:
            return "?"
        if ":" in t:
            return t.split(":")[-1]
        return t
    def set_content(self, content=None):
        print("XSDInputField::set_content {}".format(content))

