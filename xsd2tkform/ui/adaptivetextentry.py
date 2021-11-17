"""Text input widget with size adaptive height
"""

import tkinter as tk
from tkinter import ttk

class AdaptiveHeightText(tk.Text):
    def __init__(self, parent, height=None, width=None, *args, **kwargs):
        tk.Text.__init__(self, parent, height=height, width=width, *args, **kwargs)
        self.bind("<KeyRelease>", self.update_height)
    def update_height(self, event=None):
        text = self.get("1.0", tk.END)
        n_lines = len(text.split("\n"))+1
        self.configure(height=n_lines)
    def insert(self, *args, **kwargs):
        super().insert(*args, **kwargs)
        self.update_height()
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_height()

if __name__=="__main__":
    root = tk.Tk()
    mainframe = tk.Frame(root)

    text=AdaptiveHeightText(mainframe, height=2)
    text.pack(side=tk.TOP, fill=tk.X, expand=1)

    text.insert("1.0", "a\nb\nc\n")

    mainframe.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    root.mainloop()

