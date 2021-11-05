"""XSDForm definition

Forms are frames containing widgets 
"""
import tkinter as tk
from tkinter import ttk


class XSDForm(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
