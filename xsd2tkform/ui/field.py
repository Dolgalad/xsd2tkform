"""Base XSD input field definition
"""
import tkinter as tk


class XSDInputField(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
    def sanitize_type(self, t):
        if ":" in t:
            return t.split(":")[-1]
        return t

